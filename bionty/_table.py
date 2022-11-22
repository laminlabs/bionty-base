import re
from collections import namedtuple
from functools import cached_property
from pathlib import Path
from typing import Iterable, NamedTuple, Optional

import pandas as pd

from ._logger import logger
from ._ontology import Ontology
from ._settings import check_dynamicdir_exists, settings
from .dev._fix_index import (
    check_if_index_compliant,
    explode_aggregated_column_to_expand,
    get_compliant_index_from_column,
)
from .dev._io import load_yaml, url_download

HERE = Path(__file__).parent


def _camel_to_snake(string: str) -> str:
    """Convert CamelCase to snake_case."""
    return re.sub(r"(?<!^)(?=[A-Z])", "_", string).lower()


class EntityTable:
    """Biological entity as a EntityTable.

    See :doc:`guide` for background.
    """

    def __init__(self, id: str = None):
        self._id_field = "id" if id is None else id
        # By default lookup allows auto-completion for name and returns the id.
        # lookup column can be changed using `.lookup_col = `.
        self._lookup_col = "name"

    @cached_property
    def entity(self) -> str:
        """Name of the entity."""
        return _camel_to_snake(self.__class__.__name__)

    @cached_property
    def df(self) -> pd.DataFrame:
        """DataFrame representation of EntityTable."""
        raise NotImplementedError

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

        return self._namedtuple_from_dict(df[self._id_field].to_dict())

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
        return pd.DataFrame(
            [(term.id, term.name) for term in ontology.terms()],
            columns=["ontology_id", "name"],
        ).set_index(self._id_field)

    def _curate(
        self, df: pd.DataFrame, column: str = None, agg_col: str = None
    ) -> pd.DataFrame:
        """Curate index of passed DataFrame to conform with default identifier."""
        df = df.copy()

        if agg_col is not None:
            # if provided a column with aggregated values, performs alias mapping
            alias_map = explode_aggregated_column_to_expand(
                self.df.reset_index(), aggregated_col=agg_col, target_col=self._id_field
            )[self._id_field]

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
            df.index.name = self._id_field
            df[column] = orig_series.values  # keep the original column untouched
        # annotated what complies with the default ID
        df["__curated__"] = matches
        # some stats for logging
        n_misses = len(matches) - matches.sum()
        frac_misses = round(n_misses / len(matches) * 100, 1)
        n_mapped = matches.sum()
        frac_mapped = 100 - frac_misses
        logger.success(f"{n_mapped} terms ({frac_mapped}%) are linked.")
        logger.warning(f"{n_misses} terms ({frac_misses}%) are not linked.")
        return df

    @check_dynamicdir_exists
    def _ontology_download(self, url: str):
        """Download owl file to dynamicdir."""
        logger.info("Downloading ontology for the first time might take a while...")
        url_download(url, self._ontology_localpath_from_url(url))

    def _ontology_localpath_from_url(self, url: str):
        """Get version from the ontology url."""
        version = url.split("/")[-2]
        filename = url.split("/")[-1]
        return settings.dynamicdir / f"{version}|{filename}"

    def curate(self, df: pd.DataFrame, column: str = None):
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
            column = self._id_field
            df.rename(columns={orig_column: column}, inplace=True)

        return self._curate(df=df, column=column).rename(columns={column: orig_column})

    def ontology(self, namespace: str, **kwargs) -> Ontology:
        """Ontology."""
        # Get the in-use url from yaml file
        info = (
            load_yaml(HERE / "versions.yml").get(self.__class__.__name__).get(namespace)
        )
        url = info.get("versions").get(info.get("in-use"))
        if url is None:
            raise ValueError("No ontology url is provided.")
        _ontology_localpath_from_url = self._ontology_localpath_from_url(url)
        if not _ontology_localpath_from_url.exists():
            self._ontology_download(url)

        return Ontology(handle=_ontology_localpath_from_url, **kwargs)
