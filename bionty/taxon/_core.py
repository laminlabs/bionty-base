from pathlib import Path

import pandas as pd

HERE = Path(__file__).parent
SPECIES_FILENAME = HERE / "tables/Species.csv"

SPECIES_COLS = [
    "scientific_name",
    "display_name",
    "common_name",
    "taxon_id",
    "assembly",
    "accession",
    "release",
]


class Taxon:
    """Species related bio entities."""

    _df = pd.read_csv(SPECIES_FILENAME, header=0, index_col=0)

    def __init__(self, species="human"):
        self._std_name = species

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
        return SPECIES_COLS

    def search(self, field: str):
        """Search species fields based on .std_id.

        Args:
            field: str
                one of .fields
        Returns:
            value of a field

        e.g.
        'common_name': 'human'
        'scientific_name': 'homo_sapiens'
        'short_name': 'hsapiens'
        'taxon_id': 9606
        'assembly': 'GRCh38.p13'

        """
        return self._df[[field]].to_dict()[field][self.std_name]
