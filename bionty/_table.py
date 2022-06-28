from functools import cached_property
from collections import namedtuple
import pandas as pd
from enum import Enum
from typing import Protocol, Dict
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

    def __init__(id: Field = Field.field1):
        self._id_field = id

    @cached_property
    def df(self) -> pd.DataFrame:
        """DataFrame represenation of table."""
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