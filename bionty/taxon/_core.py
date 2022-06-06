from functools import cached_property
from pathlib import Path
from typing import NamedTuple

import pandas as pd
from pydantic import create_model

from .._models import Entity

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

    def __init__(self, species="human"):
        self._std_name = species

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
        return SPECIES_COLS

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
        return self._df[[field]].to_dict()[field][self.std_name]


class Entry(NamedTuple):
    name: str
    scientific_name: str
    common_name: str
    taxon_id: int
    assembly: str
    accession: str
    release: int
    short_name: str


class Organism:
    def parse_df(self):
        taxon = Taxon()

        Organism = create_model("Organism", __base__=Entity)
        for i in taxon.df.index:
            entry = {"name": taxon.df.loc[i]["scientific_name"]}
            entry.update({col: taxon.df.loc[i][col] for col in taxon.df.columns})
            setattr(
                Organism,
                taxon.df.loc[i]["scientific_name"],
                Entry(**entry),
            )

        return Organism(**{"name": "organism", "std_id": "scientific_name"})


organism = Organism().parse_df()
