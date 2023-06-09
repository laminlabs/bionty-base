from __future__ import annotations

import os
import re
from collections import namedtuple
from functools import cached_property
from typing import Dict, Iterable, List, Optional, Union

import bioregistry as br
import pandas as pd
from lamin_logger import logger
from pandas import DataFrame

from bionty._md5 import verify_md5

from ._ontology import Ontology
from ._settings import check_datasetdir_exists, check_dynamicdir_exists, settings
from .dev._fix_index import (
    check_if_index_compliant,
    explode_aggregated_column_to_expand,
    get_compliant_index_from_column,
)
from .dev._handle_sources import LAMINDB_INSTANCE_LOADED
from .dev._io import s3_bionty_assets, url_download


class Bionty:
    """Biological entity as an Bionty.

    See :doc:`guide/index` for background.
    """

    def __init__(
        self,
        source: Optional[str],
        version: Optional[str] = None,
        species: Optional[str] = None,
        *,
        reference_id: Optional[Union[BiontyField, str]] = None,
        synonyms_field: Optional[Union[BiontyField, str]] = None,
        include_id_prefixes: Optional[Dict[str, List[str]]] = None,
        include_name_prefixes: Optional[Dict[str, List[str]]] = None,
        exclude_id_prefixes: Optional[Dict[str, List[str]]] = None,
        exclude_name_prefixes: Optional[Dict[str, List[str]]] = None,
    ):
        if source is not None or version is not None:
            # We don't allow custom databases inside lamindb instances
            # because the lamindb standard should be used
            if LAMINDB_INSTANCE_LOADED:
                logger.error(
                    "Only default sources are allowed inside LaminDB instances!"
                )
                logger.hint(
                    "To use a different source, please either:\n    Close your instance"
                    " via `lamin close` \n    OR\n    Configure currently_used"
                    f" {self.__class__.__name__} source in"
                    " lnschema_bionty.BiontySource table"
                )
                self._species = None
                self._source = None
                self._version = None
                return

            if br.normalize_prefix(source):
                source = br.normalize_prefix(source)

        def _camel_to_snake(string: str) -> str:
            return re.sub(r"(?<!^)(?=[A-Z])", "_", string).lower()

        self._species = species
        self._entity = _camel_to_snake(self.__class__.__name__)
        self.reference_id = reference_id
        self._synonyms_field = synonyms_field
        self.include_id_prefixes = include_id_prefixes
        self.include_name_prefixes = include_name_prefixes
        self.exclude_id_prefixes = exclude_id_prefixes
        self.exclude_name_prefixes = exclude_name_prefixes

        self._set_attributes(source=source, version=version)

    def __repr__(self) -> str:
        representation = (
            f"{self.__class__.__name__}\n"
            f"Species: {self.species}\n"
            f"Source: {self.source}, {self.version}\n\n"
            f"📖 {self.__class__.__name__}.df(): ontology reference table\n"
            f"🔎 {self.__class__.__name__}.lookup(): autocompletion of ontology terms\n"
            f"🔗 {self.__class__.__name__}.ontology: Pronto.Ontology object"
        )
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

    @cached_property
    def ontology(self) -> Ontology:  # type:ignore
        """The Pronto Ontology object.

        See: https://pronto.readthedocs.io/en/stable/api/pronto.Ontology.html
        """
        self._download_ontology_file()
        return Ontology(handle=self._local_ontology_path)

    def df(self) -> pd.DataFrame:
        """Pandas DataFrame of the ontology.

        Returns:
            A Pandas DataFrame of the ontology indexed by the passed reference_id or "ontology_id" if not specified.

        Examples:
            >>> import bionty as bt
            >>> bt.Gene().df()
        """
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
        reference_index_name = self.reference_id
        if self.reference_id is None and "ontology_id" in df.columns:
            reference_index_name = "ontology_id"
        try:
            return df.set_index(reference_index_name)
        except KeyError:
            return df

    def lookup(self, field: str = "name") -> tuple:
        """Return an auto-complete object for the bionty id.

        Args:
            field: The field to lookup the values for. Adapt this parameter to, for example, 'ontology_id' to lookup by ID.
                   Defaults to 'name'.

        Returns:
            A NamedTuple of lookup information of the entitys values.

        Examples:
            >>> import bionty as bt
            >>> gene_lookout = bt.Gene().lookup()
            >>> gene_lookout.TEF
        """

        def to_lookup_keys(x: list) -> list:
            """Convert a list of strings to tab-completion allowed formats."""
            lookup = [re.sub("[^0-9a-zA-Z]+", "_", str(i)) for i in x]
            for i, value in enumerate(lookup):
                if value == "" or (not value[0].isalpha()):
                    lookup[i] = f"LOOKUP_{value}"
            return lookup

        def uniquefy_duplicates(lst: Iterable) -> list:
            """Uniquefy duplicated values in a list."""
            df = pd.DataFrame(lst)
            duplicated = df[df[0].duplicated(keep=False)]
            df.loc[duplicated.index, 0] = (
                duplicated[0] + "__" + duplicated.groupby(0).cumcount().astype(str)
            )
            return list(df[0].values)

        def namedtuple_from_df(df: pd.DataFrame, name: Optional[str] = None) -> tuple:
            """Create a namedtuple from a dataframe to allow autocompletion."""
            if name is None:
                name = self._entity

            nt = namedtuple(name, df.index)  # type:ignore
            return nt(
                **{
                    df.index[i]: row
                    for i, row in enumerate(df.itertuples(name=name, index=False))
                }
            )

        df = self.df().reset_index()
        if field not in df:
            raise AssertionError(f"No {field} column exists!")

        # uniquefy lookup keys
        df.index = uniquefy_duplicates(to_lookup_keys(df[field].values))

        return namedtuple_from_df(df)

    def _download_ontology_file(self) -> None:
        """Download ontology file to _local_ontology_path."""
        if not self._local_ontology_path.exists():
            logger.download(f"Downloading {self.__class__.__name__} ontology file...")
            try:
                self._url_download(self._url)
            finally:
                # Only verify md5 if it's actually available from the sources.yaml file
                if len(self._md5) > 0:
                    if not verify_md5(self._local_ontology_path, self._md5):
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
            # skip terms without id or name
            # skip obsolete terms
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

        def __flatten_prefixes(db_to_prefixes: Optional[Dict[str, List[str]]]) -> set:
            flat_prefixes = {
                prefix for values in db_to_prefixes.values() for prefix in values  # type: ignore
            }

            return flat_prefixes

        prefixes_to_filter: List[str] = []
        if self.include_id_prefixes and self.source in self.include_id_prefixes.keys():
            prefixes_to_filter.extend(__flatten_prefixes(self.include_id_prefixes))

        if (
            self.include_name_prefixes
            and self.source in self.include_name_prefixes.keys()
        ):
            prefixes_to_filter.extend(__flatten_prefixes(self.include_name_prefixes))

        if self.exclude_id_prefixes and self.source in self.exclude_id_prefixes.keys():
            prefixes_to_filter.extend(__flatten_prefixes(self.exclude_id_prefixes))

        if (
            self.exclude_name_prefixes
            and self.source in self.exclude_name_prefixes.keys()
        ):
            prefixes_to_filter.extend(__flatten_prefixes(self.exclude_name_prefixes))

        df_values = [
            val
            for val in df_values
            if all(not val[0].startswith(prefix) for prefix in prefixes_to_filter)
            or all(not val[1].startswith(prefix) for prefix in prefixes_to_filter)
        ]

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
    def _set_attributes(
        self, source: Optional[str], version: Optional[str] = None
    ) -> None:
        """Sets version, database and URL attributes for passed database and requested version.

        Args:
            source: The database to find the URL and version for.
            version: The requested version of the database.
        """
        from ._display_sources import (
            display_available_sources,
            display_currently_used_sources,
        )

        def _subset_to_entity(df: pd.DataFrame, key: str):
            if isinstance(df.loc[key], pd.Series):
                return df.loc[[key]]
            else:
                return df.loc[key]

        default_versions = _subset_to_entity(
            display_currently_used_sources(), self.__class__.__name__
        )
        all_versions = _subset_to_entity(
            display_available_sources(), self.__class__.__name__
        )

        if source is None:
            # default species is the first key in the default_versions
            self._species = (
                default_versions["species"][0] if self.species is None else self.species
            )
            # there is only one single entry for a species
            default_source_version = default_versions[
                default_versions["species"] == self.species
            ]
            source_version = default_source_version.to_dict(orient="records")
            if len(source_version) == 0:
                raise ValueError(
                    f"Species '{self.species}' is not available! Check"
                    " `bionty.display_available_sources()`!"
                )
            self._source = source_version[0].get("source_key")
            self._version = (
                source_version[0].get("version") if version is None else version
            )
        else:
            self._source = source  # type:ignore
            versions_source = all_versions[all_versions["source_key"] == source]
            if versions_source.shape[0] == 0:
                raise ValueError(
                    f"Source '{self.source}' is not available! Check"
                    " `bionty.display_available_sources()`!"
                )
            self._species = (
                versions_source["species"][0] if self.species is None else self.species
            )
            source_version = versions_source[
                versions_source["species"] == self.species
            ].to_dict(orient="records")
            if len(source_version) == 0:
                raise ValueError(
                    f"Species '{self.species}' is not available! Check"
                    " `bionty.display_available_sources()`!"
                )
            self._version = (
                source_version[0].get("version") if version is None else version
            )

        version_row = all_versions[
            (all_versions["species"] == self.species)
            & (all_versions["source_key"] == self.source)
            & (all_versions["version"] == self.version)
        ].to_dict(orient="records")
        if len(version_row) == 0:
            raise ValueError(
                f"Version '{self.version}' is not available for source '{self.source}'!"
                " Check `bionty.display_available_sources()`!"
            )
        self._url = version_row[0].get("url")
        self._md5 = version_row[0].get("md5")

        self._parquet_filename = f"{self.species}_{self.source}_{self.version}_{self.__class__.__name__}_lookup.parquet"  # noqa: E501
        self._local_parquet_path = (
            settings.dynamicdir / self._parquet_filename
        )  # noqa: W503,E501
        self._ontology_filename = f"{self.species}___{self.source}___{self.version}___{self.__class__.__name__}".replace(
            " ", "_"
        )
        self._local_ontology_path = settings.dynamicdir / self._ontology_filename

        # To also include the index field
        df = self.df()
        if df.index.name is not None:
            df = df.reset_index()
        for col_name in df.columns:
            try:
                setattr(self, col_name, BiontyField(self, col_name))
            # Some fields of an ontology (e.g. Gene) are not Bionty class attributes and must be skipped.
            except AttributeError:
                pass

    def curate(
        self,
        df: pd.DataFrame,
        column: str = None,
        reference_id: Union[BiontyField, str] = None,
        case_sensitive: bool = True,
    ) -> pd.DataFrame:
        """Curate index of passed DataFrame to conform with default identifier.

        - If `target_column` is `None`, checks the existing index for compliance
          with the default identifier.
        - If `target_column` denotes an entity identifier,
          tries to map that identifier to the default identifier.

        Args:
            df: The input Pandas DataFrame to curate.
            column: The column in the passed Pandas DataFrame to curate.
            reference_id: The reference column in the ontology Pandas DataFrame.
                             'Defaults to ontology_id'.
            case_sensitive: Whether the curation should be case sensitive or not.
                            Defaults to True.

        Returns:
            Returns the DataFrame with the curated index and a boolean `__curated__`
            column that indicates compliance with the default identifier.

        Examples:
            >>> import pandas as pd
            >>> import bionty as bt
            >>> df = pd.DataFrame(index=["Boettcher cell", "bone marrow cell"]
            >>> ct = bt.CellType()
            >>> curated_df = ct.curate(df, reference_id=ct.name)
        """
        if reference_id is None:
            reference_id = self.df().index.name  # type: ignore
        elif self.reference_id and reference_id != "ontology_id":
            reference_id = reference_id
        elif self.reference_id:
            reference_id = self.reference_id  # type: ignore

        df = df.copy()
        ref_df = self.df()
        orig_column = column
        if column is not None and column not in ref_df.columns:
            column = reference_id  # type: ignore
            df.rename(columns={orig_column: column}, inplace=True)

        # uppercasing the target column before curating
        orig_column_values = None
        if not case_sensitive:
            if column in df.columns:
                orig_column_values = df[column].values
                df[column] = df[column].str.upper()
            else:
                orig_column_values = df.index.values
                df.index = df.index.str.upper()

        curated_df = self._curate(
            df=df, column=column, reference_id=reference_id
        ).rename(columns={column: orig_column})

        # change the original column values back
        if orig_column_values is not None:
            if "orig_index" in curated_df:
                curated_df["orig_index"] = orig_column_values
            else:
                curated_df[orig_column] = orig_column_values

        return curated_df

    def _curate(
        self,
        df: pd.DataFrame,
        reference_id: Union[BiontyField, str],
        column: str = None,
        agg_col: str = None,
        inplace: bool = False,
    ) -> pd.DataFrame:
        """Curate index of passed DataFrame to conform with default identifier."""
        if reference_id is None:
            reference_id = self.reference_id  # type: ignore

        if not inplace:
            df = df.copy()
        ref_df = self.df()

        # this is needed for features parsing in lamindb
        self._parsing_id = reference_id

        if agg_col is not None:
            # if provided a column with aggregated values, performs alias mapping
            alias_map = explode_aggregated_column_to_expand(
                ref_df.reset_index(),
                aggregated_col=agg_col,
                target_col=reference_id,
            )[reference_id]

        # when column is None, use index as the input column
        if column is None:
            index_name = df.index.name
            df["__mapped_index"] = (
                df.index if agg_col is None else df.index.map(alias_map)
            )
            df["orig_index"] = df.index
            df.index = df["__mapped_index"].fillna(df["orig_index"])
            del df["__mapped_index"]
            df.index.name = index_name

            matches = check_if_index_compliant(
                df.index, ref_df.reset_index()[str(reference_id)]
            )
        else:
            orig_series = df[column]
            df[column] = df[column] if agg_col is None else df[column].map(alias_map)
            df[column] = df[column].fillna(orig_series)
            new_index, matches = get_compliant_index_from_column(
                df=df,
                ref_df=ref_df,
                column=column,
            )

            # keep the original index name as column name if exists
            # otherwise name it "orig_index"
            if df.index.name is None:
                df["orig_index"] = df.index
            else:
                df[df.index.name] = df.index
            df.index = new_index
            df.index.name = reference_id
            df[column] = orig_series.values  # keep the original column untouched
        # annotated what complies with the default ID
        df["__curated__"] = matches
        # some stats for logging
        n_misses = len(matches) - matches.sum()
        frac_misses = round(n_misses / len(matches) * 100, 1)
        n_mapped = matches.sum()
        frac_mapped = 100 - frac_misses
        logger.success(f"{n_mapped} terms ({frac_mapped}%) are mapped.")
        logger.warning(f"{n_misses} terms ({frac_misses}%) are not mapped.")

        return df

    def inspect(
        self, identifiers: Iterable, reference_id: BiontyField, return_df: bool = False
    ) -> Union[DataFrame, dict[str, list[str]]]:
        """Inspect if a list of identifiers are mappable to the entity reference.

        Args:
            identifiers: Identifiers that will be checked against the Ontology.
            reference_id: The BiontyField of the ontology to compare against.
                          Examples are 'ontology_id' to map against the ontology ID
                          or 'name' to map against the ontologies field names.
            return_df: Whether to return a Pandas DataFrame.

        Returns:
            - A Dictionary that maps the input ontology (keys) to the ontology field (values)
            - If specified A Pandas DataFrame with the curated index and a boolean `__curated__`
              column that indicates compliance with the default identifier.

        Examples:
            >>> import pandas as pd
            >>> import bionty as bt
            >>> df = pd.DataFrame(index=["Boettcher cell", "bone marrow cell"]
            >>> ct = bt.CellType()
            >>> ct.inspect(df, reference_id=ct.name)
        """
        df = pd.DataFrame(index=identifiers)

        # check if synonyms are present
        try:
            synonyms_mapper = self.map_synonyms(
                identifiers=identifiers, reference_id=reference_id, return_mapper=True
            )
            if len(synonyms_mapper) > 0:
                logger.warning("The identifiers contain synonyms!")
                logger.hint(
                    "To increase mappability, convert them into standardized"
                    " names/symbols using '.map_synonyms()'"
                )
        except Exception:
            pass

        curated_df = self._curate(
            df=df, column=None, reference_id=reference_id, inplace=False
        )

        if return_df:
            mapping_df = curated_df.rename(
                columns={"orig_index": str(reference_id), "__curated__": "__mapped__"}
            )
            return mapping_df.reset_index(drop=True)
        else:
            mapping: Dict[str, List[str]] = {}
            mapping["mapped"] = curated_df.index[curated_df["__curated__"]].tolist()
            mapping["not_mapped"] = curated_df.index[
                ~curated_df["__curated__"]
            ].tolist()

            return mapping

    def map_synonyms(
        self,
        identifiers: Iterable,
        reference_id: BiontyField,
        *,
        synonyms_field: Union[BiontyField, str] = "synonyms",
        return_mapper: bool = False,
    ) -> Union[Dict[str, str], List[str]]:
        """Maps input identifiers against Ontology synonyms.

        Args:
            identifiers: Identifiers that will be mapped against an Ontology field (BiontyField).
            reference_id: The BiontyField of ontology representing the identifiers.
            return_mapper: Whether to return a dictionary of {identifiers : <mapped reference_id values>}.

        Returns:
            - A list of mapped reference_id values if return_mapper is False.
            - A dictionary of mapped values with mappable identifiers as keys
              and values mapped to reference_id as values if return_mapper is True.

        Examples:
            >>> import pandas as pd
            >>> import bionty as bt
            >>> gene_symbols = ["A1CF", "A1BG", "FANCD1", "FANCD20"]
            >>> gn = bt.Gene(source="ensembl", version="release-108")
            >>> mapping = gn.map_synonyms(gene_symbols, gn.symbol)
        """
        reference_id_str, synonyms_field_str = str(reference_id), str(synonyms_field)

        df = self.df().reset_index()
        if reference_id_str not in df.columns:
            raise KeyError(
                f"reference_id '{reference_id_str}' is invalid! Available fields are:"
                f" {list(df.columns)}"
            )
        if synonyms_field_str not in df.columns:
            raise KeyError(
                f"synonyms_field '{synonyms_field_str}' is invalid! Available fields"
                f" are: {list(df.columns)}"
            )
        if reference_id_str == synonyms_field_str:
            raise KeyError("synonyms_field must be different from reference_id!")

        alias_map = explode_aggregated_column_to_expand(
            df,
            aggregated_col=synonyms_field_str,
            target_col=reference_id_str,
        )[reference_id_str]

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
        reference_id: BiontyField,
        synonyms_field: Union[BiontyField, str, None] = "synonyms",
        case_sensitive: bool = True,
        return_ranked_results: bool = False,
    ) -> str:
        """Fuzzy matching of a given string using RapidFuzz.

        Args:
            string: The input string to match against the reference_id ontology values.
            reference_id: The BiontyField of ontology the input string is matching against.
            synonyms_field: Also map against in the synonyms (If None, no mapping against synonyms).
            case_sensitive: Whether the match is case sensitive.
            return_ranked_results: Whether to return all entries ranked by matching ratios.

        Returns:
            Best match of the input string.

        Examples:
            >>> import bionty as bt
            >>> ct = bt.CellType()
            >>> ct.fuzzy_match("T cells", ct.name)
        """

        def _fuzz_ratio(string: str, iterable: pd.Series, case_sensitive: bool = True):
            from rapidfuzz import fuzz, utils

            if case_sensitive:
                processor = None
            else:
                processor = utils.default_process
            return iterable.apply(lambda x: fuzz.ratio(string, x, processor=processor))

        df = self.df().reset_index()
        reference_id_str = str(reference_id)
        synonyms_field_str = str(synonyms_field)

        if synonyms_field_str in df.columns:
            df_exp = explode_aggregated_column_to_expand(
                df,
                aggregated_col=synonyms_field_str,
                target_col=reference_id_str,
            ).reset_index()
            target_column = synonyms_field_str
        else:
            df_exp = df.copy()
            target_column = reference_id_str

        df_exp["__ratio__"] = _fuzz_ratio(
            string=string, iterable=df_exp[target_column], case_sensitive=case_sensitive
        )
        df_exp_grouped = (
            df_exp.groupby(reference_id_str)
            .max()
            .sort_values("__ratio__", ascending=False)
        )
        df_scored = df.set_index(reference_id_str).loc[df_exp_grouped.index]
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
