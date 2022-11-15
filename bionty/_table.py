import re
from collections import namedtuple
from functools import cached_property
from typing import Iterable, NamedTuple, Optional

import pandas as pd

from ._logger import logger
from ._ontology import Ontology
from ._settings import settings
from .dev._fix_index import (
    check_if_index_compliant,
    explode_aggregated_column_to_expand,
    get_compliant_index_from_column,
)


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

    def curate(
        self, df: pd.DataFrame, column: str = None, agg_col: str = None
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

    def ontology(
        self,
        url: Optional[str] = None,
        reload: bool = False,
        filename: Optional[str] = None,
    ) -> Ontology:
        """Ontology."""
        if url is None:
            raise ValueError("No ontology url is provided.")
        filename = url.split("/")[-1] if filename is None else filename
        ontology_path = settings.dynamicdir / filename.replace(".owl", ".obo")

        # ontology will be pulled from the url if no cached file is found
        url = url if ((not ontology_path.exists()) or (reload)) else None

        return Ontology(handle=ontology_path, url=url, filename=filename)
