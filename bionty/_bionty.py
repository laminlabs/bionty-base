from __future__ import annotations

import os
from functools import cached_property
from typing import Dict, Iterable, List, Optional, Set, Union

import pandas as pd
from lamin_logger import logger
from pandas import DataFrame

from bionty._md5 import verify_md5

from ._lookup import Lookup
from ._ontology import Ontology
from ._settings import check_datasetdir_exists, check_dynamicdir_exists, settings
from .dev._fix_index import (
    check_if_index_compliant,
    explode_aggregated_column_to_expand,
)
from .dev._handle_sources import LAMINDB_INSTANCE_LOADED
from .dev._io import s3_bionty_assets, url_download


class Bionty:
    """Biological entity as an Bionty.

    See :doc:`guide/index` for background.
    """

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
                "Only default sources below are allowed inside LaminDB"
                f" instances!\n{self._default_sources}\n"
            )
            logger.hint(
                "To use a different source, please either:\n    Close your instance"
                " via `lamin close` \n    OR\n    Configure currently_used"
                f" {self.__class__.__name__} source in"
                " lnschema_bionty.BiontySource table"
            )
            self._source = None  # type: ignore
            return

        self._set_file_paths()
        self.include_id_prefixes = include_id_prefixes

        # df is only read into memory at the init to improve performance
        self._df = None
        df = self.df()
        if df.index.name is not None:
            # To also include the index fields
            df = df.reset_index()
        for col_name in df.columns:
            try:
                setattr(self, col_name, BiontyField(self, col_name))
            # Some fields of an ontology (e.g. Gene) are not Bionty class attributes and must be skipped.
            except AttributeError:
                pass
        self._df = df

    def __repr__(self) -> str:
        # fmt: off
        representation = (
            f"{self.__class__.__name__}\n"
            f"Species: {self.species}\n"
            f"Source: {self.source}, {self.version}\n\n"
            f"📖 {self.__class__.__name__}.df(): ontology reference table\n"
            f"🔎 {self.__class__.__name__}.lookup(): autocompletion of ontology terms\n"
            f"🎯 {self.__class__.__name__}.fuzzy_match(): fuzzy match against ontology terms\n"
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
    def ontology(self) -> Ontology:  # type:ignore
        """The Pronto Ontology object.

        See: https://pronto.readthedocs.io/en/stable/api/pronto.Ontology.html
        """
        self._download_ontology_file()
        return Ontology(handle=self._local_ontology_path)

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
        """TODO."""
        lc = locals()

        # kwargs that are not None
        kwargs = {
            k: lc.get(k)
            for k in ["source", "version", "species"]
            if lc.get(k) is not None
        }
        keys = list(kwargs.keys())

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
            if len(keys) == 0:
                curr = self._default_sources.head(1).to_dict(orient="records")[0]
                kwargs = {
                    k: v
                    for k, v in curr.items()
                    if k in ["species", "source", "version"]
                }
            row = self._all_sources[
                (self._all_sources["species"] == kwargs["species"])
                & (self._all_sources["source"] == kwargs["source"])
                & (self._all_sources["version"] == kwargs["version"])
            ].head(1)

        if row.shape[0] == 0:
            raise ValueError(
                f"No source is available with {kwargs}\nCheck"
                " `bionty.display_available_sources()`"
            )
        return row.to_dict(orient="records")[0]

    def _download_ontology_file(self) -> None:
        """Download ontology file to _local_ontology_path."""
        if not self._local_ontology_path.exists():
            logger.download(f"Downloading {self.__class__.__name__} ontology file...")
            try:
                self._url_download(self._url)
            finally:
                # Only verify md5 if it's actually available from the sources.yaml file
                if len(self._md5) > 0:  # type: ignore
                    if not verify_md5(self._local_ontology_path, self._md5):  # type: ignore
                        logger.warning(
                            f"MD5 sum for {self._local_ontology_path} did not match"
                            f" {self._md5}! Redownloading..."
                        )
                        os.remove(self._local_ontology_path)
                        self._url_download(self._url)

    def _ontology_to_df(self, ontology: Ontology):
        """Convert pronto.Ontology to a DataFrame with columns id, name, children."""
        df_values = []
        for term in ontology.terms():
            # skip terms without id or name and obsolete terms
            if (not term.id) or (not term.name) or term.obsolete:
                continue

            # term definition text
            definition = None if term.definition is None else term.definition.title()

            # concatenate synonyms into a string
            synonyms = "|".join(
                [i.description for i in term.synonyms if i.scope == "EXACT"]
            )
            if len(synonyms) == 0:
                synonyms = None  # type:ignore

            # get 1st degree children as a list
            subclasses = [
                s.id for s in term.subclasses(distance=1, with_self=False).to_set()
            ]

            df_values.append((term.id, term.name, definition, synonyms, subclasses))

        if self.include_id_prefixes and self.source in list(
            self.include_id_prefixes.keys()
        ):
            flat_include_id_prefixes = {
                prefix1 for values in self.include_id_prefixes.values() for prefix1 in values  # type: ignore
            }
            df_values = list(
                filter(
                    lambda val: any(
                        val[0].startswith(prefix) for prefix in flat_include_id_prefixes
                    ),
                    df_values,
                )
            )

        df = pd.DataFrame(
            df_values,
            columns=["ontology_id", "name", "definition", "synonyms", "children"],
        ).set_index("ontology_id")

        # needed to avoid erroring in .lookup()
        df["name"].fillna("", inplace=True)

        return df

    @check_dynamicdir_exists
    def _url_download(self, url: str) -> str:
        """Download file from url to dynamicdir _local_ontology_path."""
        # Try to download from s3://bionty-assets
        s3_bionty_assets(
            filename=self._ontology_filename,
            assets_base_url="s3://bionty-assets",
            localpath=self._local_ontology_path,
        )

        # If the file is not available, download from the url
        if not self._local_ontology_path.exists():
            logger.download(
                f"Downloading {self.__class__.__name__} ontology file from: {url}"
            )
            url_download(url, self._local_ontology_path)

        return self._local_ontology_path

    @check_datasetdir_exists
    def _set_file_paths(self) -> None:
        """Sets version, database and URL attributes for passed database and requested version.

        Args:
            source: The database to find the URL and version for.
            version: The requested version of the database.
        """
        self._url = self._source_record.get("url")
        self._md5 = self._source_record.get("md5")

        self._parquet_filename = f"{self.species}_{self.source}_{self.version}_{self.__class__.__name__}_lookup.parquet"  # noqa: E501
        self._local_parquet_path = (
            settings.dynamicdir / self._parquet_filename
        )  # noqa: W503,E501
        self._ontology_filename = f"{self.species}___{self.source}___{self.version}___{self.__class__.__name__}".replace(
            " ", "_"
        )
        self._local_ontology_path = settings.dynamicdir / self._ontology_filename

    def df(self) -> pd.DataFrame:
        """Pandas DataFrame of the ontology.

        Returns:
            A Pandas DataFrame of the ontology.

        Examples:
            >>> import bionty as bt
            >>> bt.Gene().df()
        """
        if self._df is None:
            # Download and sync from s3://bionty-assets
            s3_bionty_assets(
                filename=self._parquet_filename,
                assets_base_url="s3://bionty-assets",
                localpath=self._local_parquet_path,
            )
            # If download is not possible, write a parquet file from ontology
            if not self._local_parquet_path.exists():
                # write df to parquet file
                df = self._ontology_to_df(self.ontology)
                df.to_parquet(self._local_parquet_path)

            # loads the df and set index
            df = pd.read_parquet(self._local_parquet_path).reset_index()
            if "ontology_id" in df.columns:
                return df.set_index("ontology_id")
            else:
                return df
        else:
            return self._df

    def lookup(self, field: Union[BiontyField, str] = "name") -> Lookup:
        """Return an auto-complete object for the bionty field.

        Args:
            field: The field to lookup the values for.
                   Defaults to 'name'.

        Returns:
            A NamedTuple of lookup information of the field values.

        Examples:
            >>> import bionty as bt
            >>> gene_bionty_lookup = bt.Gene().lookup()
            >>> gene_bionty_lookup['ADGB-DT']
        """
        df = self.df()

        field = str(field)
        if field not in df.columns:
            raise AssertionError(f"No {field} column exists!")

        # This implementation only returns the last row if multiple rows
        # match the same field value i
        df_dict = {}
        for i, row in enumerate(
            df.itertuples(index=False, name=self.__class__.__name__)
        ):
            df_dict[df[field][i]] = row

        return Lookup(df_dict)

    def inspect(
        self, identifiers: Iterable, field: BiontyField, return_df: bool = False
    ) -> Union[DataFrame, Dict[str, List[str]]]:
        """Inspect if a list of identifiers are mappable to the entity reference.

        Args:
            identifiers: Identifiers that will be checked against the Ontology.
            field: The BiontyField of the ontology to compare against.
                          Examples are 'ontology_id' to map against the ontology ID
                          or 'name' to map against the ontologies field names.
            return_df: Whether to return a Pandas DataFrame.

        Returns:
            - A Dictionary that maps the input ontology (keys) to the ontology field (values)
            - If specified A Pandas DataFrame with the curated index and a boolean `__mapped__`
              column that indicates compliance with the default identifier.

        Examples:
            >>> import bionty as bt
            >>> celltype_bionty = bt.CellType()
            >>> celltype_bionty.inspect(["Boettcher cell", "bone marrow cell"], field=celltype_bionty.name)
        """
        mapped_df = pd.DataFrame(index=identifiers)

        try:
            synonyms_mapper = self.map_synonyms(
                identifiers=identifiers, field=field, return_mapper=True
            )
            if len(synonyms_mapper) > 0:
                logger.warning("The identifiers contain synonyms!")
                logger.hint(
                    "To increase mappability, convert them into standardized"
                    " names/symbols using '.map_synonyms()'"
                )
        except Exception:
            pass

        matches = check_if_index_compliant(mapped_df.index, self.df()[str(field)])

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
        field: BiontyField,
        *,
        synonyms_field: Union[BiontyField, str] = "synonyms",
        return_mapper: bool = False,
    ) -> Union[Dict[str, str], List[str]]:
        """Maps input identifiers against Ontology synonyms.

        Args:
            identifiers: Identifiers that will be mapped against an Ontology field (BiontyField).
            field: The BiontyField of ontology representing the identifiers.
            return_mapper: Whether to return a dictionary of {identifiers : <mapped field values>}.

        Returns:
            - A list of mapped field values if return_mapper is False.
            - A dictionary of mapped values with mappable identifiers as keys
              and values mapped to field as values if return_mapper is True.

        Examples:
            >>> import bionty as bt
            >>> gene_bionty = bt.Gene(source="ensembl", version="release-108")
            >>> gene_symbols = ["A1CF", "A1BG", "FANCD1", "FANCD20"]
            >>> mapping = gene_bionty.map_synonyms(gene_symbols, gn.symbol)
        """
        field_str, synonyms_field_str = str(field), str(synonyms_field)

        df = self.df()
        if field_str not in df.columns:
            raise KeyError(
                f"field '{field_str}' is invalid! Available fields are:"
                f" {list(df.columns)}"
            )
        if synonyms_field_str not in df.columns:
            raise KeyError(
                f"synonyms_field '{synonyms_field_str}' is invalid! Available fields"
                f" are: {list(df.columns)}"
            )
        if field_str == synonyms_field_str:
            raise KeyError("synonyms_field must be different from field!")

        alias_map = explode_aggregated_column_to_expand(
            df,
            aggregated_col=synonyms_field_str,
            target_col=field_str,
        )[field_str]

        if return_mapper:
            mapped_dict = {
                item: alias_map.get(item)
                for item in identifiers
                if alias_map.get(item) is not None and alias_map.get(item) != item
            }
            return mapped_dict
        else:
            mapped_list = [alias_map.get(item, item) for item in identifiers]
            return mapped_list

    def fuzzy_match(
        self,
        string: str,
        field: Union[BiontyField, str] = "name",
        synonyms_field: Union[BiontyField, str, None] = "synonyms",
        case_sensitive: bool = True,
        return_ranked_results: bool = False,
    ) -> pd.DataFrame:
        """Fuzzy matching of a given string against a Bionty field.

        Args:
            string: The input string to match against the field ontology values.
            field: The BiontyField of ontology the input string is matching against.
            synonyms_field: Also map against in the synonyms (If None, no mapping against synonyms).
            case_sensitive: Whether the match is case sensitive.
            return_ranked_results: Whether to return all entries ranked by matching ratios.

        Returns:
            Best match of the input string.

        Examples:
            >>> import bionty as bt
            >>> celltype_bionty = bt.CellType()
            >>> celltype_bionty.fuzzy_match("gamma delta T cell")
        """

        def _fuzz_ratio(string: str, iterable: pd.Series, case_sensitive: bool = True):
            from rapidfuzz import fuzz, utils

            if case_sensitive:
                processor = None
            else:
                processor = utils.default_process
            return iterable.apply(lambda x: fuzz.ratio(string, x, processor=processor))

        df = self.df()
        field_str = str(field)
        synonyms_field_str = str(synonyms_field)

        if synonyms_field_str in df.columns:
            df_exp = explode_aggregated_column_to_expand(
                df,
                aggregated_col=synonyms_field_str,
                target_col=field_str,
            ).reset_index()
            target_column = synonyms_field_str
        else:
            df_exp = df.copy()
            target_column = field_str

        df_exp["__ratio__"] = _fuzz_ratio(
            string=string, iterable=df_exp[target_column], case_sensitive=case_sensitive
        )
        df_exp_grouped = (
            df_exp.groupby(field_str).max().sort_values("__ratio__", ascending=False)
        )
        df_exp_grouped = df_exp_grouped[df_exp_grouped.index.isin(df[field_str])]
        df_scored = df.set_index(field_str).loc[df_exp_grouped.index]
        df_scored["__ratio__"] = df_exp_grouped["__ratio__"]

        if return_ranked_results:
            return df_scored.sort_values("__ratio__", ascending=False)
        else:
            return df_scored[df_scored["__ratio__"] == df_scored["__ratio__"].max()]


class BiontyField:
    def __init__(self, parent: Bionty, name: str):
        self.parent = parent
        self.name = name

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
