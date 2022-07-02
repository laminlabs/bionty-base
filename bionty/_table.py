from collections import namedtuple
from enum import Enum
from functools import cached_property

import pandas as pd

from ._logging import logger
from .dev._fix_index import check_if_index_compliant, get_compliant_index_from_column


class Field(str, Enum):
    field1 = "field1"
    field2 = "field2"


class EntityTable:
    """Biological entity as a EntityTable.

    See :doc:`tutorials/index` for background.
    """

    def __init__(self, id: Field = Field.field1):
        self._id_field = id

    @cached_property
    def df(self) -> pd.DataFrame:
        """DataFrame representation of EntityTable."""
        raise NotImplementedError

    def lookup(self, field):
        """Return an auto-complete object for a given field."""
        return namedtuple(field, self.df[field])

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
        if column is None:
            matches = check_if_index_compliant(df.index, self.df.index)
        else:
            new_index, matches = get_compliant_index_from_column(
                df=df,
                ref_df=self.df,
                column=column,
            )

            if df.index.name is None:
                df["orig_index"] = df.index
            else:
                df[df.index.name] = df.index
            df.index = new_index
            df.index.name = self._id_field
        # annotated what complies with the default ID
        df["__curated__"] = matches
        # some stats for logging
        n_misses = len(matches) - matches.sum()
        frac_misses = round(n_misses / len(matches) * 100, 1)
        logger.warning(f"{n_misses} terms ({frac_misses}%) are not mappable.")
        return df
