import os
import re
from collections import namedtuple
from functools import cached_property
from pathlib import Path
from typing import Dict, Iterable, Literal, Optional

import bioregistry as br
import pandas as pd
from lamin_logger import logger

from bionty._md5 import verify_md5

from ._ontology import Ontology
from ._settings import check_datasetdir_exists, check_dynamicdir_exists, settings
from .dev._fix_index import (
    check_if_index_compliant,
    explode_aggregated_column_to_expand,
    get_compliant_index_from_column,
)
from .dev._io import load_yaml, url_download

VERSIONS_PATH = Path(__file__).parent / "versions"


def _camel_to_snake(string: str) -> str:
    """Convert CamelCase to snake_case."""
    return re.sub(r"(?<!^)(?=[A-Z])", "_", string).lower()


class Entity:
    """Biological entity as an Entity.

    See :doc:`guide/index` for background.
    """

    def __init__(
        self,
        database: Optional[str],
        version: Optional[str] = None,
        species: Optional[str] = None,
        *,
        prefix: Optional[str] = None,
        reference_id: Optional[str] = None,
    ):
        # By default lookup allows auto-completion for the `name` field.
        # lookup column can be changed using `.lookup_field = `.
        self._lookup_field = "name"
        self._species = "human" if species is None else species
        self.prefix = prefix
        self.reference_id = reference_id

        if database:
            # We don't allow custom databases inside lamindb instances
            # because the lamindb standard should be used
            if os.getenv("LAMINDB_INSTANCE_LOADED") == 1:
                raise ValueError(
                    "Custom databases are not allowed inside lamindb instances."
                    "Check active databases using `bionty.display_active_versions`."
                )

            if br.normalize_prefix(database):
                database = br.normalize_prefix(database)
        self._set_attributes(database=database, version=version)

    def __repr__(self) -> str:
        representation = (
            f"Entity of {self.__class__.__name__}\n"
            f"Species: {self.species}\n"
            f"Database: {self.database}\n\n"
            f"Access ontology terms with '{self.__class__.__name__}.df'"
        )
        return representation

    @property
    def database(self) -> str:
        """Name of the database."""
        return self._database

    @cached_property
    def entity(self) -> str:
        """Name of the entity."""
        return _camel_to_snake(self.__class__.__name__)

    @property
    def species(self):
        """The `name` of `Species` Entity."""
        return self._species

    @property
    def version(self):
        """The `name` of `version` entity Entity."""
        return self._version

    @cached_property
    def ontology(self, **kwargs) -> Ontology:  # type:ignore
        """The Pronto Ontology object."""
        localpath = self._url_download(self._url)

        return Ontology(handle=localpath, **kwargs)

    @cached_property
    def df(self) -> pd.DataFrame:
        """Pandas DataFrame."""
        # download
        if not self._local_parquet_path.exists():
            try:
                self._url_download(self._url)
            finally:
                # Only verify md5 if it's actually available
                if len(self._md5) > 0:
                    if not verify_md5(self._ontology_download_path, self._md5):
                        logger.warning(
                            f"MD5 sum for {self._ontology_download_path} did not match"
                            f" {self._md5}! Redownloading..."
                        )
                        os.remove(self._ontology_download_path)
                        self._url_download(self._url)
            # write df to parquet file
            df = self._ontology_to_df(self.ontology)
            df.to_parquet(self._local_parquet_path)

        # loads the df and set index
        df = pd.read_parquet(self._local_parquet_path).reset_index()
        if self.reference_id is None and "ontology_id" in df.columns:
            self.reference_id = "ontology_id"
        try:
            return df.set_index(self.reference_id)
        except KeyError:
            return df

    @property
    def lookup_field(self) -> str:
        """The column that allows auto-completion."""
        return self._lookup_field

    @lookup_field.setter
    def lookup_field(self, column_name) -> None:
        """Set the lookup field."""
        self._lookup_field = column_name

    @cached_property
    def lookup(self) -> tuple:
        """Return an auto-complete object for the bionty id."""
        df = self.df.reset_index()
        if self._lookup_field not in df:
            raise AssertionError(f"No {self._lookup_field} column exists!")

        # uniquefy lookup keys
        df.index = self._uniquefy_duplicates(
            self._to_lookup_keys(df[self._lookup_field].values)
        )

        return self._namedtuple_from_dict(df)

    def _to_lookup_keys(self, x: list) -> list:
        """Convert a list of strings to tab-completion allowed formats."""
        lookup = [re.sub("[^0-9a-zA-Z]+", "_", str(i)) for i in x]
        for i, value in enumerate(lookup):
            if not value[0].isalpha():
                lookup[i] = f"LOOKUP_{value}"
        return lookup

    def _namedtuple_from_dict(
        self, df: pd.DataFrame, name: Optional[str] = None
    ) -> tuple:
        """Create a namedtuple from a dict to allow autocompletion."""
        if name is None:
            name = self.entity
        nt = namedtuple(name, df.index)  # type:ignore
        return nt(
            **{
                df.index[i]: row
                for i, row in enumerate(df.itertuples(name=name, index=False))
            }
        )

    def _uniquefy_duplicates(self, lst: Iterable) -> list:
        """Uniquefy duplicated values in a list."""
        df = pd.DataFrame(lst)
        duplicated = df[df[0].duplicated(keep=False)]
        df.loc[duplicated.index, 0] = (
            duplicated[0] + "__" + duplicated.groupby(0).cumcount().astype(str)
        )
        return list(df[0].values)

    def _ontology_to_df(self, ontology: Ontology):
        """Convert ontology to a DataFrame with ontology_id and name columns."""
        if self.prefix:
            df = pd.DataFrame(
                [
                    (term.id, term.name)
                    for term in ontology.terms()
                    if term.id.startswith(f"{self.prefix}:")
                ],
                columns=["ontology_id", "name"],
            ).set_index("ontology_id")
        else:
            df = pd.DataFrame(
                [(term.id, term.name) for term in ontology.terms()],
                columns=["ontology_id", "name"],
            ).set_index("ontology_id")

        df["name"].fillna("", inplace=True)
        return df

    @check_dynamicdir_exists
    def _url_download(self, url: str):
        """Download file from url to dynamicdir."""
        if not self._ontology_download_path.exists():
            logger.info(
                f"Downloading {self.entity} reference for the first time might take a"
                " while..."
            )
            url_download(url, self._ontology_download_path)

        return self._ontology_download_path

    def _ontology_localpath_from_url(self, url: str):
        """Get version from the ontology url."""
        version = url.split("/")[-2]
        filename = url.split("/")[-1]
        return settings.dynamicdir / f"{version}___{filename}"

    def _load_versions(
        self, source: Literal["versions", "local"] = "local"
    ) -> Dict[str, Dict[str, Dict]]:
        """Load all versions with string version keys."""
        YAML_PATH = (
            Path(f"{VERSIONS_PATH}/versions.yaml")
            if source == "versions"
            else Path(f"{settings.versionsdir}/local.yaml")
        )
        versions = load_yaml(YAML_PATH).get(self.__class__.__name__)

        versions_db: Dict[str, Dict[str, Dict]] = {}

        for db, vers in versions.items():
            versions_db[db] = {"versions": {}}
            for k in vers["versions"]:
                versions_db[db]["versions"][str(k)] = versions[db]["versions"][k]

        return versions_db

    @check_datasetdir_exists
    def _set_attributes(
        self, database: Optional[str], version: Optional[str] = None
    ) -> None:
        """Sets version, database and URL attributes for passed database and requested version.

        Args:
            database: The database to find the URL and version for.
            version: The requested version of the database.
        """
        current_defaults = (
            "._lndb.yaml"
            if os.getenv("LAMINDB_INSTANCE_LOADED") == 1
            else "._current.yaml"
        )

        ((current_database, current_version),) = (
            load_yaml(VERSIONS_PATH / current_defaults)
            .get(self.__class__.__name__)
            .items()
        )

        available_db_versions = self._load_versions(source="local")

        # Use the latest version if version is None.
        self._database = current_database if database is None else str(database)
        # Only the database was passed -> get the latest version from the available db versions  # noqa: E501
        if database and not version:
            self._version = next(
                iter(available_db_versions[self._database]["versions"])
            )
        else:
            self._version = current_version if version is None else str(version)
        self._url, self._md5 = (
            available_db_versions.get(self._database).get("versions").get(self._version)  # type: ignore  # noqa: E501
        )
        if self._url is None:
            raise ValueError(
                f"Database {self._database} version {self._version} is not found,"
                f" select one of the following: {available_db_versions}"
            )

        self._cloud_parquet_path = f"{self.species}_{self.database}_{self.version}_{self.__class__.__name__}_lookup.parquet"  # noqa: E501
        self._local_parquet_path = (
            settings.datasetdir / self._cloud_parquet_path
        )  # noqa: W503,E501
        self._ontology_download_path = (
            settings.dynamicdir
            / f"{self.species}_{self.database}_{self.version}_{self.__class__.__name__}___{self._url.split('/')[-1]}"  # noqa: E501 W503
        )

    def curate(
        self,
        df: pd.DataFrame,
        column: str = None,
        reference_id: str = "ontology_id",
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
        """
        if self.reference_id and reference_id != "ontology_id":
            reference_id = reference_id
        elif self.reference_id:
            reference_id = self.reference_id

        df = df.copy()
        orig_column = column
        if column is not None and column not in self.df.columns:
            column = reference_id
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
        reference_id: str = "ontology_id",
        column: str = None,
        agg_col: str = None,
    ) -> pd.DataFrame:
        """Curate index of passed DataFrame to conform with default identifier."""
        df = df.copy()
        # this is needed for features parsing in lamindb
        self._parsing_id = reference_id

        if agg_col is not None:
            # if provided a column with aggregated values, performs alias mapping
            alias_map = explode_aggregated_column_to_expand(
                self.df.reset_index(),
                aggregated_col=agg_col,
                target_col=reference_id,
            )[reference_id]

        if column is None:
            # when column is None, use index as the input column
            index_name = df.index.name
            df["__mapped_index"] = (
                df.index if agg_col is None else df.index.map(alias_map)
            )
            df["orig_index"] = df.index
            df.index = df["__mapped_index"].fillna(df["orig_index"])
            del df["__mapped_index"]
            df.index.name = index_name
            matches = check_if_index_compliant(
                df.index, self.df.reset_index()[reference_id]
            )
        else:
            orig_series = df[column]
            df[column] = df[column] if agg_col is None else df[column].map(alias_map)
            df[column] = df[column].fillna(orig_series)
            new_index, matches = get_compliant_index_from_column(
                df=df,
                ref_df=self.df,
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
