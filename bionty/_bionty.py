from __future__ import annotations

import os
from functools import cached_property
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Set, Tuple, Union

import pandas as pd
from lamin_logger import logger
from lamin_logger._lookup import Lookup

from bionty._md5 import verify_md5

from ._ontology import Ontology
from ._settings import check_datasetdir_exists, check_dynamicdir_exists, settings
from .dev._handle_sources import LAMINDB_INSTANCE_LOADED
from .dev._io import s3_bionty_assets, url_download


class Bionty:
    """Bionty base model."""

    def __init__(
        self,
        source: Optional[str] = None,
        version: Optional[str] = None,
        species: Optional[str] = None,
        *,
        include_id_prefixes: Optional[Dict[str, List[str]]] = None,
    ):
        self._fetch_sources()
        # match user input species, source and version with yaml
        self._source_record = self._match_all_sources(
            source=source, version=version, species=species
        )
        self._species = self._source_record["species"]
        self._source = self._source_record["source"]
        self._version = self._source_record["version"]

        # only currently_used sources are allowed inside lamindb instances
        default_sources = list(self._default_sources.itertuples(index=False, name=None))
        if (
            LAMINDB_INSTANCE_LOADED()
            and (self.species, self.source, self.version) not in default_sources
        ):
            logger.error(
                f"Only default sources below are allowed inside LaminDB instances!\n{self._default_sources}\n"  # noqa: E501
            )
            # fmt: off
            logger.hint(
                f"To use a different source, please either:\n"
                f"    Close your instance via `lamin close`\n"
                f"    OR\n"
                f"    Configure currently_used {self.__class__.__name__} source in `lnschema_bionty.BiontySource`"
            )
            # fmt: on
            self._source = None  # type: ignore
            return

        self._set_file_paths()
        self.include_id_prefixes = include_id_prefixes

        # df is only read into memory at the init to improve performance
        df = self._load_df()
        # self._df has no index
        if df.index.name is not None:
            df = df.reset_index()
        self._df = df

        # set column names/fields as attributes
        for col_name in self._df.columns:
            try:
                setattr(self, col_name, BiontyField(self, col_name))
            # Some fields of an ontology (e.g. Gene) are not Bionty class attributes and must be skipped.
            except AttributeError:
                pass

    def __repr__(self) -> str:
        # fmt: off
        representation = (
            f"{self.__class__.__name__}\n"
            f"Species: {self.species}\n"
            f"Source: {self.source}, {self.version}\n\n"
            f"📖 {self.__class__.__name__}.df(): ontology reference table\n"
            f"🔎 {self.__class__.__name__}.lookup(): autocompletion of terms\n"
            f"🎯 {self.__class__.__name__}.search(): free text search of terms\n"
            f"🧐 {self.__class__.__name__}.inspect(): check if identifiers are mappable\n"
            f"👽 {self.__class__.__name__}.map_synonyms(): map synonyms to standardized names\n"
            f"🔗 {self.__class__.__name__}.ontology: Pronto.Ontology object"
        )
        # fmt: on
        if self._source is not None:
            return representation
        else:
            return "invalid Bionty object"

    @property
    def species(self):
        """The `name` of `Species` Bionty."""
        return self._species

    @property
    def source(self):
        """Name of the source."""
        return self._source

    @property
    def version(self):
        """The `name` of `version` entity Bionty."""
        return self._version

    @property
    def fields(self) -> Set:
        """All Bionty entity fields."""
        blacklist = {"include_id_prefixes"}
        fields = set(
            [
                field
                for field in vars(self)
                if not callable(getattr(self, field)) and not field.startswith("_")
            ]
        )
        return fields - blacklist

    @cached_property
    def ontology(self):
        """The Pronto Ontology object.

        See: https://pronto.readthedocs.io/en/stable/api/pronto.Ontology.html
        """
        if self._local_ontology_path is None:
            logger.error(f"{self.__class__.__name__} has no Pronto Ontology object!")
            return
        else:
            self._download_ontology_file(
                localpath=self._local_ontology_path,
                url=self._url,
                md5=self._md5,
            )
            return Ontology(handle=self._local_ontology_path)

    def _download_ontology_file(self, localpath: Path, url: str, md5: str = "") -> None:
        """Download ontology file to _local_ontology_path."""
        if not localpath.exists():
            logger.download(f"Downloading {self.__class__.__name__} ontology file...")
            try:
                self._url_download(url, localpath)
            finally:
                # Only verify md5 if it's actually available from the sources.yaml file
                if len(md5) > 0:
                    if not verify_md5(localpath, md5):
                        logger.warning(
                            f"MD5 sum for {localpath} did not match {md5}. Redownloading..."  # noqa: E501
                        )
                        os.remove(localpath)
                        self._url_download(url, localpath)

    def _fetch_sources(self) -> None:
        from ._display_sources import (
            display_available_sources,
            display_currently_used_sources,
        )

        def _subset_to_entity(df: pd.DataFrame, key: str):
            return df.loc[[key]] if isinstance(df.loc[key], pd.Series) else df.loc[key]

        self._default_sources = _subset_to_entity(
            display_currently_used_sources(), self.__class__.__name__
        )

        self._all_sources = _subset_to_entity(
            display_available_sources(), self.__class__.__name__
        )

    def _match_all_sources(
        self,
        source: Optional[str] = None,
        version: Optional[str] = None,
        species: Optional[str] = None,
    ) -> Dict[str, str]:
        """Match a source record base on passed species, source and version."""
        lc = locals()

        # kwargs that are not None
        kwargs = {
            k: lc.get(k)
            for k in ["source", "version", "species"]
            if lc.get(k) is not None
        }
        keys = list(kwargs.keys())

        # if 1 or 2 kwargs are specified, find the best match in all sources
        if (len(kwargs) == 1) or (len(kwargs) == 2):
            cond = self._all_sources[keys[0]] == kwargs.get(keys[0])
            if len(kwargs) == 1:
                row = self._all_sources[cond].head(1)
            else:
                # len(kwargs) == 2
                cond = getattr(cond, "__and__")(
                    self._all_sources[keys[1]] == kwargs.get(keys[1])
                )
                row = self._all_sources[cond].head(1)
        else:
            # if no kwargs are passed, take the currently used source record
            if len(keys) == 0:
                curr = self._default_sources.head(1).to_dict(orient="records")[0]
                kwargs = {
                    k: v
                    for k, v in curr.items()
                    if k in ["species", "source", "version"]
                }
            # if all 3 kwargs are specified, match the record from all sources
            # do the same for the kwargs that obtained from default source to obtain url
            row = self._all_sources[
                (self._all_sources["species"] == kwargs["species"])
                & (self._all_sources["source"] == kwargs["source"])
                & (self._all_sources["version"] == kwargs["version"])
            ].head(1)

        # if no records matched the passed kwargs, raise error
        if row.shape[0] == 0:
            raise ValueError(
                f"No source is available with {kwargs}\nCheck"
                " `bionty.display_available_sources()`"
            )
        return row.to_dict(orient="records")[0]

    @check_dynamicdir_exists
    def _url_download(self, url: str, localpath: Path) -> None:
        """Download file from url to dynamicdir _local_ontology_path."""
        # Try to download from s3://bionty-assets
        s3_bionty_assets(
            filename=self._ontology_filename,
            assets_base_url="s3://bionty-assets",
            localpath=localpath,
        )

        # If the file is not available, download from the url
        if not localpath.exists():
            logger.download(
                f"Downloading {self.__class__.__name__} ontology file from: {url}"
            )
            _ = url_download(url, localpath)

    @check_datasetdir_exists
    def _set_file_paths(self) -> None:
        """Sets version, database and URL attributes for passed database and requested version.

        Args:
            source: The database to find the URL and version for.
            version: The requested version of the database.
        """
        self._url = self._source_record.get("url", "")
        self._md5 = self._source_record.get("md5", "")

        # parquet file name
        self._parquet_filename = f"{self.species}_{self.source}_{self.version}_{self.__class__.__name__}_lookup.parquet"  # noqa: E501
        # parquet file local path
        self._local_parquet_path = settings.dynamicdir / self._parquet_filename
        # ontology file name
        self._ontology_filename = f"{self.species}___{self.source}___{self.version}___{self.__class__.__name__}".replace(
            " ", "_"
        )

        if self._url.endswith(".parquet"):  # user provide reference table as the url
            # no local ontology file
            self._local_ontology_path = None
            if not self._url.startswith("s3://bionty-assets/"):
                self._parquet_filename = None  # type:ignore
        else:
            self._local_ontology_path = settings.dynamicdir / self._ontology_filename

    def _get_default_field(
        self, field: Optional[Union[BiontyField, str]] = None
    ) -> str:
        """Default to name field."""
        if field is None:
            if "name" in self._df.columns:
                field = "name"
            elif "symbol" in self._df.columns:
                field = "symbol"
            else:
                raise ValueError("Please specify a field!")
        field = str(field)
        if field not in self._df.columns:
            raise AssertionError(f"No {field} column exists!")
        return field

    def _load_df(self) -> pd.DataFrame:
        # Download and sync from s3://bionty-assets
        if self._parquet_filename is None:
            # download url as the parquet file
            self._url_download(self._url, self._local_parquet_path)
        else:
            s3_bionty_assets(
                filename=self._parquet_filename,
                assets_base_url="s3://bionty-assets",
                localpath=self._local_parquet_path,
            )
        # If download is not possible, write a parquet file from ontology
        if not self._local_parquet_path.exists():
            # write df to parquet file
            df = self.ontology.to_df(
                source=self.source, include_id_prefixes=self.include_id_prefixes
            )
            df.to_parquet(self._local_parquet_path)

        # loads the df and reset index
        df = pd.read_parquet(self._local_parquet_path)
        return df

    def df(self) -> pd.DataFrame:
        """Pandas DataFrame of the ontology.

        Returns:
            A Pandas DataFrame of the ontology.

        Examples:
            >>> import bionty as bt
            >>> bt.Gene().df()
        """
        if "ontology_id" in self._df.columns:
            return self._df.set_index("ontology_id")
        else:
            return self._df

    def inspect(
        self, identifiers: Iterable, field: BiontyField, return_df: bool = False
    ) -> Union[pd.DataFrame, Dict[str, List[str]]]:
        """Inspect if a list of identifiers are mappable to the entity reference.

        Args:
            identifiers: Identifiers that will be checked against the field.
            field: The BiontyField of the ontology to compare against.
                          Examples are 'ontology_id' to map against the ontology ID
                          or 'name' to map against the ontologies field names.
            return_df: Whether to return a Pandas DataFrame.

        Returns:
            - A Dictionary of "mapped" and "unmapped" identifiers
            - If `return_df`: A DataFrame indexed by identifiers with a boolean `__mapped__`
              column that indicates compliance with the identifiers.

        Examples:
            >>> import bionty as bt
            >>> gene_bionty = bt.Gene()
            >>> gene_symbols = ["A1CF", "A1BG", "FANCD1", "FANCD20"]
            >>> gene_bionty.inspect(gene_symbols, field=gene_bionty.symbol)
        """
        mapped_df = pd.DataFrame(index=identifiers)

        try:
            synonyms_mapper = self.map_synonyms(
                identifiers=identifiers, field=field, return_mapper=True
            )
            if len(synonyms_mapper) > 0:
                logger.warning(
                    "The identifiers contain synonyms!\n   To increase mappability,"
                    " standardize them via '.map_synonyms()'"
                )
        except Exception:
            pass

        # check if index is compliant
        matches = mapped_df.index.isin(self._df[str(field)])

        # annotated what complies with the default ID
        mapped_df["__mapped__"] = matches

        def unique_rm_empty(idx: pd.Index):
            idx = idx.unique()
            return idx[(idx != "") & (~idx.isnull())]

        mapped = unique_rm_empty(mapped_df.index[mapped_df["__mapped__"]]).tolist()
        unmapped = unique_rm_empty(mapped_df.index[~mapped_df["__mapped__"]]).tolist()

        n_mapped = len(mapped)
        n_unmapped = len(unmapped)
        n_unique_terms = len(mapped) + len(unmapped)
        n_empty = len(matches) - n_unique_terms
        frac_unmapped = round(n_unmapped / len(matches) * 100, 1)
        frac_mapped = 100 - frac_unmapped

        if n_empty > 0:
            logger.warning(
                f"Received {n_unique_terms} unique terms, {n_empty} empty/duplicated"
                " terms are ignored."
            )
        logger.success(f"{n_mapped} terms ({frac_mapped}%) are mapped.")
        logger.warning(f"{n_unmapped} terms ({frac_unmapped}%) are not mapped.")

        if return_df:
            return mapped_df
        else:
            mapping: Dict[str, List[str]] = {}
            mapping["mapped"] = mapped
            mapping["not_mapped"] = unmapped
            return mapping

    def map_synonyms(
        self,
        identifiers: Iterable,
        *,
        return_mapper: bool = False,
        synonyms_field: Union[BiontyField, str] = "synonyms",
        synonyms_sep: str = "|",
        field: Optional[Union[BiontyField, str]] = None,
    ) -> Union[Dict[str, str], List[str]]:
        """Maps input identifiers against synonyms.

        Args:
            identifiers: Identifiers that will be mapped against an Ontology field (BiontyField).
            return_mapper: Whether to return a dictionary of {identifiers : <mapped field values>}.
            synonyms_field: The BiontyField representing the concatenated synonyms.
            synonyms_sep: Which separator is used to separate synonyms.
            field: The BiontyField representing the identifiers.

        Returns:
            - A list of mapped field values if return_mapper is False.
            - A dictionary of mapped values with mappable identifiers as keys
              and values mapped to field as values if return_mapper is True.

        Examples:
            >>> import bionty as bt
            >>> gene_bionty = bt.Gene()
            >>> gene_symbols = ["A1CF", "A1BG", "FANCD1", "FANCD20"]
            >>> standardized_symbols = gene_bionty.map_synonyms(gene_symbols, gn.symbol)
        """
        from lamin_logger._map_synonyms import map_synonyms

        return map_synonyms(
            df=self._df,
            identifiers=identifiers,
            field=self._get_default_field(field),
            return_mapper=return_mapper,
            synonyms_field=str(synonyms_field),
            sep=synonyms_sep,
        )

    def lookup(self, field: Optional[Union[BiontyField, str]] = None) -> Tuple:
        """An auto-complete object for a Bionty field.

        Args:
            field: The field to lookup the values for.
                   Defaults to 'name'.

        Returns:
            A NamedTuple of lookup information of the field values.

        Examples:
            >>> import bionty as bt
            >>> lookup = bt.CellType().lookup()
            >>> lookup.cd103_positive_dendritic_cell
            >>> lookup_dict = lookup.dict()
            >>> lookup['CD103-positive dendritic cell']
        """
        return Lookup(
            df=self._df,
            field=self._get_default_field(field),
            tuple_name=self.__class__.__name__,
            prefix="bt",
        ).lookup()

    def search(
        self,
        string: str,
        field: Optional[Union[BiontyField, str]] = None,
        top_hit: bool = False,
        case_sensitive: bool = True,
        synonyms_field: Union[BiontyField, str, None] = "synonyms",
        synonyms_sep: str = "|",
    ) -> pd.DataFrame:
        """Search a given string against a Bionty field.

        Args:
            string: The input string to match against the field values.
            field: The BiontyField of ontology the input string is matching against.
            top_hit: Default is False, return all entries ranked by matching ratios.
                If True, only return the top match.
            case_sensitive: Whether the match is case sensitive.
            synonyms_field: By default also search against the synonyms (If None, skips search).
            synonyms_sep: Which separator is used to separate synonyms.

        Returns:
            Ranked search results.

        Examples:
            >>> import bionty as bt
            >>> celltype_bionty = bt.CellType()
            >>> celltype_bionty.search("gamma delta T cell")
        """
        from lamin_logger._search import search

        return search(
            df=self._df,
            string=string,
            field=self._get_default_field(field),
            return_ranked_results=not top_hit,
            case_sensitive=case_sensitive,
            synonyms_field=str(synonyms_field),
            synonyms_sep=synonyms_sep,
            tuple_name=self.__class__.__name__,
        )


class BiontyField:
    """Field of a Bionty model."""

    def __init__(self, parent: Bionty, name: str):
        self.parent = parent
        self.name = name

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
