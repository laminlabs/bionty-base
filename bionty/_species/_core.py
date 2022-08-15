from enum import Enum
from functools import cached_property
from pathlib import Path

import pandas as pd

from .._table import EntityTable

HERE = Path(__file__).parent
SPECIES_FILENAME = HERE / "tables/Species.csv"


class Field(str, Enum):
    """Species field names."""

    common_name = "common_name"
    scientific_name = "scientific_name"
    taxon_id = "taxon_id"


class Species(EntityTable):
    """Species.

    Args:
        id: Field name that should constitute the primary reference for each
            value. It will also be the primary key in the corresponding SQL EntityTable.
    """

    def __init__(self, id: Field = Field.common_name):
        self._id_field: Field = id  # type: ignore

    @cached_property
    def df(self) -> pd.DataFrame:
        """DataFrame."""
        # we want all columns to be read in as str
        # all numeric types in the EntityTable are versions & IDs
        # they behave like strings as, for instance, they cannot be added
        # if we wouldn't do this, we couldn't also properly aggregate in the groupby
        df = pd.read_csv(SPECIES_FILENAME, header=0, dtype=str)
        # we'll use the display_name as common_name as it's unique
        df = df.drop("common_name", axis=1)
        df.rename(columns={"display_name": "common_name"}, inplace=True)
        # we'll lower case and _ concat the common name
        df.common_name = (
            df.common_name.str.lower()
            .str.translate({ord(c): "" for c in "!@#$%^&*()[]{};:,/<>?|`~=+'\""})
            .str.translate({ord(c): "_" for c in "-. "})
        )
        # we'll also drop nan as otherwise accession will raise a warning/error
        # there is a very small number of accession numbers that are nan
        df = df.dropna()
        # let's now do a groupby to get a unique index
        df = df.groupby(self._id_field).agg("; ".join)
        return df
