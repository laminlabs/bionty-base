import os
import re
from collections import namedtuple
from pathlib import Path
from typing import Dict, Iterable, Literal, NamedTuple, Optional

import bioregistry as br
import pandas as pd
from cached_property import cached_property
from lamin_logger import logger

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
        id: Optional[str] = None,
        version: Optional[str] = None,
        species: Optional[str] = None,
        filenames: Optional[Dict[str, str]] = None,
        *,
        prefix: Optional[str] = None,
    ):
        self._id = "id" if id is None else id
        # By default lookup allows auto-completion for name and returns the id.
        # lookup column can be changed using `.lookup_col = `.
        self._lookup_col = "name"
        self._species = "human" if species is None else species
        self.filenames = filenames if filenames else None
        self.prefix = prefix

        if database:
            # We don't allow custom databases inside lamindb instances
            # because the lamindb standard should be used
            if os.getenv("LAMINDB_INSTANCE_LOADED") == 1:
                raise ValueError(
                    "Custom databases are not allowed inside lamindb instances."
                    "Check active databases using `bionty.display_active_versions`."
                )

            database = br.normalize_prefix(database)
        self._set_attributes(database=database, version=version)

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
        if not self._filepath.exists():
            df = self._ontology_to_df(self.ontology)
            df.to_parquet(self._filepath)

        return pd.read_parquet(self._filepath).reset_index().set_index(self._id)

    @property
    def lookup_col(self) -> str:
        """The column that allows auto-completion."""
        return self._lookup_col

    @lookup_col.setter
    def lookup_col(self, column_name) -> None:
        self._lookup_col = column_name

    @cached_property
    def lookup(self) -> NamedTuple:
        """Return an auto-complete object for the bionty id."""
        df = self.df.reset_index()
        if self._lookup_col not in df:
            raise AssertionError(f"No {self._lookup_col} column exists!")

        # uniquefy lookup keys
        df.index = self._uniquefy_duplicates(
            self._to_lookup_keys(df[self._lookup_col].values)
        )

        return self._namedtuple_from_dict(df[self._id].to_dict())

    def _to_lookup_keys(self, x: list) -> list:
        """Convert a list of strings to tab-completion allowed formats."""
        lookup = [re.sub("[^0-9a-zA-Z]+", "_", str(i)) for i in x]
        for i, value in enumerate(lookup):
            if not value[0].isalpha():
                lookup[i] = f"LOOKUP_{value}"
        return lookup

    def _namedtuple_from_dict(
        self, mydict: dict, name: Optional[str] = None
    ) -> NamedTuple:
        """Create a namedtuple from a dict to allow autocompletion."""
        if name is None:
            name = self.entity
        nt = namedtuple(name, mydict)  # type:ignore
        return nt(**mydict)

    def _uniquefy_duplicates(self, lst: Iterable) -> list:
        """Uniquefy duplicated values in a list."""
        df = pd.DataFrame(lst)
        duplicated = df[df[0].duplicated(keep=False)]
        df.loc[duplicated.index, 0] = (
            duplicated[0] + "__" + duplicated.groupby(0).cumcount().astype(str)
        )
        return list(df[0].values)

    def _ontology_to_df(self, ontology: Ontology):
        """Convert ontology to a DataFrame with id and name columns."""
        if self.prefix:
            return pd.DataFrame(
                [
                    (term.id, term.name)
                    for term in ontology.terms()
                    if term.id.startswith(f"{self.prefix}:")
                ],
                columns=["ontology_id", "name"],
            ).set_index(self._id)
        else:
            return pd.DataFrame(
                [(term.id, term.name) for term in ontology.terms()],
                columns=["ontology_id", "name"],
            ).set_index(self._id)

    def _curate(
        self, df: pd.DataFrame, column: str = None, agg_col: str = None
    ) -> pd.DataFrame:
        """Curate index of passed DataFrame to conform with default identifier."""
        df = df.copy()

        if agg_col is not None:
            # if provided a column with aggregated values, performs alias mapping
            alias_map = explode_aggregated_column_to_expand(
                self.df.reset_index(), aggregated_col=agg_col, target_col=self._id
            )[self._id]

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
            matches = check_if_index_compliant(df.index, self.df.index)
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
            df.index.name = self._id
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

    @check_dynamicdir_exists
    def _url_download(self, url: str):
        """Download file from url to dynamicdir."""
        filename = url.split("/")[-1]
        if not self._localpath(filename).exists():
            logger.info(
                f"Downloading {self.entity} reference for the first time might take a"
                " while..."
            )
            url_download(url, self._localpath(filename))
        return self._localpath(filename)

    def _ontology_localpath_from_url(self, url: str):
        """Get version from the ontology url."""
        version = url.split("/")[-2]
        filename = url.split("/")[-1]
        return settings.dynamicdir / f"{version}___{filename}"

    def _load_versions(
        self, source: Literal["versions", "_local"] = "_local"
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

        available_db_versions = self._load_versions(source="_local")

        # Use the latest version if version is None.
        self._version = current_version if version is None else str(version)
        self._database = current_database if database is None else str(database)
        self._url = (
            available_db_versions.get(self._database).get("versions").get(self._version)  # type: ignore  # noqa: E501
        )
        if self._url is None:
            raise ValueError(
                f"Database {self._database} version {self._version} is not found,"
                f" select one of the following: {available_db_versions}"
            )

        self._cloud_file_path = f"{self.species}_{self.database}_{self.version}_{self.__class__.__name__}_lookup.parquet"  # noqa: E501
        self._filepath = settings.datasetdir / self._cloud_file_path  # noqa: W503,E501

    def _localpath(self, filename: str):
        """Return the local path of a filename marked with version."""
        return settings.dynamicdir / f"{self._version}___{filename}"

    def curate(
        self, df: pd.DataFrame, column: str = None, case_sensitive: bool = True
    ) -> pd.DataFrame:
        """Curate index of passed DataFrame to conform with default identifier.

        - If `column` is `None`, checks the existing index for compliance with
          the default identifier.
        - If `column` denotes an entity identifier, tries to map that identifier
          to the default identifier.

        Returns the DataFrame with the curated index and a boolean `__curated__`
        column that indicates compliance with the default identifier.
        """
        df = df.copy()
        orig_column = column
        if column is not None and column not in self.df.columns:
            column = self._id
            df.rename(columns={orig_column: column}, inplace=True)

        if not case_sensitive:
            if column in df.columns:
                df[column] = df[column].str.upper()
            else:
                df.index = df.index.str.upper()
        return self._curate(df=df, column=column).rename(columns={column: orig_column})
