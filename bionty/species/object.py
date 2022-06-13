from functools import cached_property
from pathlib import Path

import pandas as pd

HERE = Path(__file__).parent
SPECIES_FILENAME = HERE / "tables/Species.csv"


class Species:
    """Species class."""

    def __init__(self, common_name="human") -> None:
        self._std_name = common_name

    @cached_property
    def df(self):
        self._df = pd.read_csv(SPECIES_FILENAME, header=0, index_col=0)
        return self._df

    @property
    def std_id(self):
        """common_name is the standardized id for species."""
        return "display_name"

    @property
    def std_name(self):
        """Value of the .std_id."""
        return self._std_name

    @property
    def fields(self):
        return self.df.columns.tolist()

    def search(self, field: str):
        """Search species fields based on .std_id.

        Args:
            field: one of .fields
        Returns:
            value of a field

        e.g.
        'common_name': 'human'
        'scientific_name': 'homo_sapiens'
        'short_name': 'hsapiens'
        'taxon_id': 9606
        'assembly': 'GRCh38.p13'

        """
        return self.df[[field]].to_dict()[field][self.std_name]
