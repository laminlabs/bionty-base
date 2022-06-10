from functools import cached_property
from pathlib import Path
from typing import Any, NamedTuple

import pandas as pd

from .._models import Entity, create_model

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


def _create_species_model():
    df = pd.read_csv(SPECIES_FILENAME, header=0, index_col=0)
    Species = create_model("Species", __base__=Entity)
    for i in df.index:
        entry = {"name": df.loc[i]["scientific_name"]}
        entry.update({col: df.loc[i][col] for col in df.columns})
        Species.add_fields(**{df.loc[i]["scientific_name"]: (Entry, Entry(**entry))})
    return Species


class Entry(NamedTuple):
    name: str
    scientific_name: str
    common_name: str
    taxon_id: int
    assembly: str
    accession: str
    release: int
    short_name: str


class _Species:
    """Object oriented Species class."""

    def __init__(self, species="human") -> None:
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
        return self.df[[field]].to_dict()[field][self.std_name]


SpeciesModel: Any = _create_species_model()


class Species(SpeciesModel):
    def __call__(self, **kwds):
        return _Species(**kwds)


species = Species(**{"name": "species", "std_id": "scientific_name"})
