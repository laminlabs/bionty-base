from collections import namedtuple
from enum import Enum
from functools import cached_property

import pandas as pd

from ._logger import logger
from .dev._fix_index import (
    check_if_index_compliant,
    explode_aggregated_column_to_expand,
    get_compliant_index_from_column,
)


def _todict(x: list) -> dict:
    """Convert a list of strings to tab-completion allowed formats."""
    mapper = {
        i.translate({ord(c): "_" for c in "-. !@#$%^&*()[]{};:,/<>?|`~=+'\""}).rstrip(
            "@"
        ): i
        for i in x
    }
    for k in list(mapper.keys()):
        if k[0].isdigit():
            mapper[f"LOOKUP_{k}"] = mapper.pop(k)
    return mapper


class Field(str, Enum):
    field1 = "field1"
    field2 = "field2"


class EntityTable:
    """Biological entity as a EntityTable.

    See :doc:`tutorials` for background.
    """

    def __init__(self, id: Field = Field.field1):
        self._id_field = id

    @cached_property
    def df(self) -> pd.DataFrame:
        """DataFrame representation of EntityTable."""
        raise NotImplementedError

    @cached_property
    def lookup(self):
        """Return an auto-complete object for the bionty id."""
        values = _todict(self.df.index.to_list())
        nt = namedtuple("id", values.keys())

        return nt(**values)

    @cached_property
    def ontology(self):
        """Ontology."""
        return NotImplementedError

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
        logger.warning(f"{n_misses} terms ({frac_misses}%) are not mappable.")
        return df
