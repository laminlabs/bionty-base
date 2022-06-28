from collections import namedtuple
from enum import Enum
from functools import cached_property
from typing import Dict, Protocol

import pandas as pd
from pydantic import BaseModel


class DataClass(Protocol):
    # as already noted in comments, checking for this attribute is currently
    # the most reliable way to ascertain that something is a dataclass
    __dataclass_fields__: Dict


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
        """DataFrame representation of table."""  # nopep257
        raise NotImplementedError

    def lookup(self, field):
        """Return an auto-complete object for a given field."""
        return namedtuple(field, self.df[field])

    @cached_property
    def dc(self) -> DataClass:
        """Dataclass representation of table."""
        raise NotImplementedError

    @cached_property
    def bm(self) -> BaseModel:
        """BaseModel constructed from dataclass."""
        raise NotImplementedError

    @cached_property
    def sqlm(self):
        """SQLModel constructed from BaseModel."""
        raise NotImplementedError
