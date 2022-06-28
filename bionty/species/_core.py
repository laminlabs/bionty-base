from pathlib import Path
from enum import Enum
from functools import cached_property
import pandas as pd

HERE = Path(__file__).parent
SPECIES_FILENAME = HERE / "tables/Species.csv"


class Fields(str, Enum):
    "Species field names."
    common_name = "common_name"
    scientific_name = "scientific_name"
    taxon_id = "taxon_id"


class Species:
    """Species.

    Args:
        id: Field name that should constitute the primary reference for each
            value. It will also be the primary key in the corresponding SQL table.
    """

    def __init__(self, id: Fields = Fields.common_name):
        self._id_field = id

    @cached_property
    def df(self) -> pd.DataFrame:
        """DataFrame."""
        # we want all columns to be read in as str
        # all numeric types in the table are versions & IDs
        # they behave like strings as, for instance, they cannot be added
        # if we wouldn't do this, we couldn't also properly aggegrate in the groupby
        df = pd.read_csv(SPECIES_FILENAME, header=0, dtype=str)
        # we'll drop the display name as it's redundant with common_name
        df = df.drop("display_name", axis=1)
        # we'll lower case and _ concat the common name
        df.common_name = df.common_name.str.replace(" ", "_").str.lower()
        # we'll also drop nan as otherwise accession will raise a warning/error
        # there is a very small number of accession numbers that are nan
        df = df.dropna()
        # let's now do a groupby to get a unique index
        df = df.groupby("common_name").agg(", ".join)
        return df
