from __future__ import annotations

import logging
import os
from functools import cached_property
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Dict,
    Iterable,
    List,
    Literal,
    Optional,
    Set,
    Tuple,
    Union,
)

import numpy as np
import pandas as pd
from lamin_utils import logger
from lamin_utils._lookup import Lookup

from ._ontology import Ontology
from ._settings import check_datasetdir_exists, check_dynamicdir_exists, settings
from .dev._handle_sources import LAMINDB_INSTANCE_LOADED
from .dev._io import s3_bionty_assets, url_download
from .dev._md5 import verify_md5

if TYPE_CHECKING:
    from .dev import InspectResult


def encode_filenames(
    organism: str, source: str, version: str, entity: Union[Bionty, str]
) -> Tuple[str, str]:
    """Encode names of the cached files."""
    if isinstance(entity, Bionty):
        entity_name = entity.__class__.__name__
    else:
        entity_name = entity
    parquet_filename = f"df_{organism}__{source}__{version}__{entity_name}.parquet"
    ontology_filename = (
        f"ontology_{organism}__{source}__{version}__{entity_name}".replace(" ", "_")
    )

    return parquet_filename, ontology_filename


class Bionty:
    """Bionty base model."""

    def __init__(
        self,
        source: Optional[str] = None,
        version: Optional[str] = None,
        organism: Optional[str] = None,
        *,
        include_id_prefixes: Optional[Dict[str, List[str]]] = None,
        **kwargs,
    ):
        # backward compat for species -> organism
        if organism is None and kwargs.get("species") is not None:
            organism = kwargs.get("species")
        self._fetch_sources()
        try:
            # match user input organism, source and version with currently used sources
            current = self._match_sources(
                self._current_sources,
                source=source,
                version=version,
                organism=organism,
            )
            source = current.get("source")
            version = current.get("version")
            organism = current.get("organism")
        except ValueError:
            if LAMINDB_INSTANCE_LOADED():
                logger.warning("loading non-default source inside a LaminDB instance")
                # fmt: off
                logger.hint(
                    f"please consider:\n"
                    f"    close your instance via `lamin close` and use Bionty stand alone\n"
                    f"    OR\n"
                    f"    modify currently_used {self.__class__.__name__} source in `lnschema_bionty.BiontySource`"
                )
                # fmt: on

        # search in all available sources to get url and md5
        self._source_record = self._match_sources(
            self._all_sources,
            source=source,
            version=version,
            organism=organism,
        )

        self._organism = self._source_record["organism"]
        self._source = self._source_record["source"]
        self._version = self._source_record["version"]

        self._set_file_paths()
        self.include_id_prefixes = include_id_prefixes

        # df is only read into memory at the init to improve performance
        df = self._load_df()
        # self._df has no index
        if df.index.name is not None:
            df = df.reset_index()
        self._df: pd.DataFrame = df

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
            f"Organism: {self.organism}\n"
            f"Source: {self.source}, {self.version}\n"
            f"#terms: {self._df.shape[0] if hasattr(self, '_df') else ''}\n\n"
            f"📖 {self.__class__.__name__}.df(): ontology reference table\n"
            f"🔎 {self.__class__.__name__}.lookup(): autocompletion of terms\n"
            f"🎯 {self.__class__.__name__}.search(): free text search of terms\n"
            f"✅ {self.__class__.__name__}.validate(): strictly validate values\n"
            f"🧐 {self.__class__.__name__}.inspect(): full inspection of values\n"
            f"👽 {self.__class__.__name__}.standardize(): convert to standardized names\n"
            f"🪜 {self.__class__.__name__}.diff(): difference between two versions\n"
            f"🔗 {self.__class__.__name__}.ontology: Pronto.Ontology object"
        )
        # fmt: on
        return representation

    @property
    def organism(self):
        """The `name` of `Organism` Bionty."""
        return self._organism

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
        """Download ontology source file to _local_ontology_path."""
        if not localpath.exists():
            logger.info(
                f"downloading {self.__class__.__name__} ontology source file..."
            )
            try:
                self._url_download(url, localpath)
            finally:
                # Only verify md5 if it's actually available from the sources.yaml file
                if len(md5) > 0:
                    if not verify_md5(localpath, md5):
                        logger.warning(
                            f"MD5 sum for {localpath} did not match {md5}. re-downloading..."  # noqa: E501
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

        self._current_sources = _subset_to_entity(
            display_currently_used_sources(), self.__class__.__name__
        )

        self._all_sources = _subset_to_entity(
            display_available_sources(), self.__class__.__name__
        )

    def _match_sources(
        self,
        ref_sources: pd.DataFrame,
        source: Optional[str] = None,
        version: Optional[str] = None,
        organism: Optional[str] = None,
    ) -> Dict[str, str]:
        """Match a source record base on passed organism, source and version."""
        lc = locals()

        # kwargs that are not None
        kwargs = {
            k: lc.get(k)
            for k in ["source", "version", "organism"]
            if lc.get(k) is not None
        }
        keys = list(kwargs.keys())

        # if 1 or 2 kwargs are specified, find the best match in currently used sources
        if (len(kwargs) == 1) or (len(kwargs) == 2):
            cond = ref_sources[keys[0]] == kwargs.get(keys[0])
            if len(kwargs) == 1:
                row = ref_sources[cond].head(1)
            else:
                # len(kwargs) == 2
                cond = getattr(cond, "__and__")(
                    ref_sources[keys[1]] == kwargs.get(keys[1])
                )
                row = ref_sources[cond].head(1)
        else:
            # if no kwargs are passed, take the currently used source record
            if len(keys) == 0:
                curr = ref_sources.head(1).to_dict(orient="records")[0]
                kwargs = {
                    k: v
                    for k, v in curr.items()
                    if k in ["organism", "source", "version"]
                }
            # if all 3 kwargs are specified, match the record from currently used sources
            # do the same for the kwargs that obtained from default source to obtain url
            row = ref_sources[
                (ref_sources["organism"] == kwargs["organism"])
                & (ref_sources["source"] == kwargs["source"])
                & (ref_sources["version"] == kwargs["version"])
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
            filename=self._ontology_filename,  # type: ignore
            assets_base_url="s3://bionty-assets",
            localpath=localpath,
        )

        # If the file is not available, download from the url
        if not localpath.exists():
            logger.info(
                f"downloading {self.__class__.__name__} source file from: {url}"
            )
            _ = url_download(url, localpath)

    @check_datasetdir_exists
    def _set_file_paths(self) -> None:
        """Sets version, database and URL attributes for passed database and requested version."""
        self._url: str = self._source_record.get("url", "")
        self._md5: str = self._source_record.get("md5", "")

        # parquet file name, ontology source file name
        self._parquet_filename, self._ontology_filename = encode_filenames(
            organism=self.organism,
            source=self.source,
            version=self.version,
            entity=self,
        )
        self._local_parquet_path: Path = settings.dynamicdir / self._parquet_filename

        if self._url.endswith(".parquet"):  # user provide reference table as the url
            # no local ontology source file
            self._local_ontology_path = None  # type:ignore
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
        if self._parquet_filename is None:
            self._url_download(self._url, self._local_parquet_path)
        else:
            s3_bionty_assets(
                filename=self._parquet_filename,
                assets_base_url="s3://bionty-assets",
                localpath=self._local_parquet_path,
            )
        # If download is not possible, write a parquet file of the ontology df
        if not self._url.endswith("parquet"):
            if not self._local_parquet_path.exists():
                df = self.ontology.to_df(
                    source=self.source, include_id_prefixes=self.include_id_prefixes
                )
                df.to_parquet(self._local_parquet_path)

        # Loading the parquet file resets the index
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

    def validate(
        self,
        values: Iterable,
        field: BiontyField,
        *,
        mute: bool = False,
        **kwargs,
    ) -> np.ndarray:
        """Validate a list of values against a field of entity reference."""
        from lamin_utils._inspect import validate

        if isinstance(values, str):
            values = [values]

        field_values = self._df[str(field)]
        return validate(
            identifiers=values,
            field_values=field_values,
            case_sensitive=True,
            mute=mute,
            **kwargs,
        )

    def inspect(
        self,
        values: Iterable,
        field: BiontyField,
        *,
        mute: bool = False,
        **kwargs,
    ) -> "InspectResult":
        """Inspect a list of values against a field of entity reference.

        Args:
            values: Identifiers that will be checked against the field.
            field: The BiontyField of the ontology to compare against.
                   Examples are 'ontology_id' to map against the source ID
                   or 'name' to map against the ontologies field names.
            return_df: Whether to return a Pandas DataFrame.

        Returns:
            - A Dictionary of "validated" and "not_validated" identifiers
            - If `return_df`: A DataFrame indexed by identifiers with a boolean
                `__validated__` column indicating compliance validation.

        Examples:
            >>> import bionty as bt
            >>> gene_bt = bt.Gene()
            >>> gene_symbols = ["A1CF", "A1BG", "FANCD1", "FANCD20"]
            >>> gene_bt.inspect(gene_symbols, field=gene_bt.symbol)
        """
        from lamin_utils._inspect import inspect

        if isinstance(values, str):
            values = [values]

        return inspect(
            df=self._df,
            identifiers=values,
            field=str(field),
            mute=mute,
            **kwargs,
        )

    # unfortunately, the doc string here is duplicated with ORM.standardize
    def standardize(
        self,
        values: Iterable,
        *,
        return_mapper: bool = False,
        case_sensitive: bool = False,
        mute: bool = False,
        keep: Literal["first", "last", False] = "first",
        synonyms_field: Union[BiontyField, str] = "synonyms",
        field: Optional[Union[BiontyField, str]] = None,
    ) -> Union[Dict[str, str], List[str]]:
        """Convert into standardized names.

        Args:
            synonyms: `Iterable` Synonyms that will be standardized.
            return_mapper: `bool = False` If `True`, returns `{input_synonym1:
                standardized_name1}`.
            case_sensitive: `bool = False` Whether the mapping is case sensitive.
            organism: `Optional[str]` Map only against this organism related entries.
            keep: `Literal["first", "last", False] = "first"` When a synonym maps to
                multiple names, determines which duplicates to mark as
                `pd.DataFrame.duplicated`

                    - "first": returns the first mapped standardized name
                    - "last": returns the last mapped standardized name
                    - `False`: returns all mapped standardized name
            synonyms_field: `str = "synonyms"` A field containing the concatenated synonyms.
            field: `Optional[str]` The field representing the standardized names.

        Returns:
            If `return_mapper` is `False`: a list of standardized names. Otherwise,
            a dictionary of mapped values with mappable synonyms as keys and
            standardized names as values.

        Examples:
            >>> import bionty as bt
            >>> gene_bt = bt.Gene()
            >>> gene_symbols = ["A1CF", "A1BG", "FANCD1", "FANCD20"]
            >>> standardized_symbols = gene_bt.standardize(gene_symbols, gene_bt.symbol)
        """
        from lamin_utils._map_synonyms import map_synonyms

        if isinstance(values, str):
            values = [values]

        return map_synonyms(
            df=self._df,
            identifiers=values,
            field=self._get_default_field(field),
            return_mapper=return_mapper,
            case_sensitive=case_sensitive,
            mute=mute,
            keep=keep,
            synonyms_field=str(synonyms_field),
        )

    def map_synonyms(
        self,
        values: Iterable,
        *,
        return_mapper: bool = False,
        case_sensitive: bool = False,
        keep: Literal["first", "last", False] = "first",
        synonyms_field: Union[BiontyField, str] = "synonyms",
        field: Optional[Union[BiontyField, str]] = None,
    ) -> Union[Dict[str, str], List[str]]:
        """Maps input synonyms to standardized names."""
        logger.warning("`map_synonyms()` is deprecated, use `.standardize()`!'")
        return self.standardize(
            values=values,
            return_mapper=return_mapper,
            case_sensitive=case_sensitive,
            keep=keep,
            synonyms_field=synonyms_field,
            field=field,
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
        *,
        field: Optional[Union[BiontyField, str]] = None,
        limit: Optional[int] = None,
        case_sensitive: bool = False,
        synonyms_field: Union[BiontyField, str, None] = "synonyms",
    ) -> pd.DataFrame:
        """Search a given string against a Bionty field.

        Args:
            string: The input string to match against the field values.
            field: The BiontyField of the ontology the input string is matching against.
            top_hit: Default is False, return all entries ranked by matching ratios.
                If True, only return the top match.
            case_sensitive: Whether the match is case sensitive.
            synonyms_field: By default also search against the synonyms (If None, skips search).

        Returns:
            Ranked search results.

        Examples:
            >>> import bionty as bt
            >>> celltype_bt = bt.CellType()
            >>> celltype_bt.search("gamma delta T cell")
        """
        from lamin_utils._search import search

        return search(
            df=self._df,
            string=string,
            field=self._get_default_field(field),
            limit=limit,
            case_sensitive=case_sensitive,
            synonyms_field=str(synonyms_field),
        )

    def diff(self, compare_to: Bionty, **kwargs) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Determines a diff between two Bionty objects' ontologies.

        Args:
            compare_to: Bionty object that must be of the same class as the calling object.
            kwargs: Are passed to pd.DataFrame.compare()

        Returns:
            A tuple of two DataFrames:
            1. New entries.
            2. A pd.DataFrame.compare result which denotes all changes in `self` and `other`.

        Examples:
            >>> import bionty as bt
            >>> disease_bt_1 = bt.Disease(source="mondo", version="2023-04-04")
            >>> disease_bt_2 = bt.Disease(source="mondo", version="2023-04-04")
            >>> new_entries, modified_entries = disease_bt_1.diff(disease_bt_2)
            >>> print(new_entries.head())
            >>> print(modified_entries.head())
        """
        if not type(self) is type(compare_to):
            raise ValueError("Both Bionty objects must be of the same class.")

        if not self.source == compare_to.source:
            raise ValueError("Both Bionty objects must use the same source.")

        if self.version == compare_to.version:
            raise ValueError("The versions of the Bionty objects must differ.")

        # The 'parents' column (among potentially others) contain Numpy array values.
        # We transform them to tuples to determine the diff.
        def _convert_arrays_to_tuples(arr):  # pragma: no cover
            if isinstance(arr, np.ndarray):
                return tuple(arr)
            else:
                return arr

        for bt_obj in [self, compare_to]:
            for column in bt_obj.df().columns:
                if any(isinstance(val, np.ndarray) for val in bt_obj.df()[column]):
                    bt_obj._df[column] = bt_obj.df()[column].apply(
                        _convert_arrays_to_tuples
                    )

        # New entries
        new_entries = pd.concat([self.df(), compare_to.df()]).drop_duplicates(
            keep=False
        )

        # Changes in existing entries
        common_index = self.df().index.intersection(compare_to.df().index)
        self_df_common = self.df().loc[common_index]
        compare_to_df_common = compare_to.df().loc[common_index]
        modified_entries = self_df_common.compare(compare_to_df_common, **kwargs)

        logging.info(f"{len(new_entries)} new entries were added.")
        logging.info(f"{len(modified_entries)} entries were modified.")

        return new_entries, modified_entries


class BiontyField:
    """Field of a Bionty model."""

    def __init__(self, parent: Bionty, name: str):
        self.parent = parent
        self.name = name

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
