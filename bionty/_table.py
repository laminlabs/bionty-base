from collections import namedtuple
from enum import Enum
from functools import cached_property

import pandas as pd


class Field(str, Enum):
    field1 = "field1"
    field2 = "field2"


class Table:
    """Biological entity as a table.

    See :doc:`tutorial/index` for background.
    """

    def __init__(self, id: Field = Field.field1):
        self._id_field = id

    @cached_property
    def df(self) -> pd.DataFrame:
        """DataFrame representation of table."""
        raise NotImplementedError

    def lookup(self, field):
        """Return an auto-complete object for a given field."""
        return namedtuple(field, self.df[field])
