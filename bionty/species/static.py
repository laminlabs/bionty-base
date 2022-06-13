from typing import Any, NamedTuple

from .._models import Entity, create_model
from .object import Species


def _create_species_model(std_id="scientific_name"):
    df = Species().df.reset_index()
    SpeciesData = create_model("SpeciesData", __base__=Entity)
    for i in df.index:
        entry = {
            "name": df.loc[i][std_id],
        }
        entry.update({col: df.loc[i][col] for col in df.columns})
        SpeciesData.add_fields(**{df.loc[i][std_id]: (Entry, Entry(**entry))})
    return SpeciesData


class Entry(NamedTuple):
    name: str  # this is the value of std_id, aka scientific_name
    display_name: str
    scientific_name: str
    common_name: str
    taxon_id: int
    assembly: str
    accession: str
    release: int
    short_name: str


SpeciesDataModel: Any = _create_species_model()


class SpeciesModel(SpeciesDataModel):
    def __call__(self, **kwargs):
        return Species(**kwargs)


species = SpeciesModel(**{"name": "species", "std_id": "scientific_name"})
"""Access point to species.

`species` -> a static class containing species as fields
`species()` -> an instance of bionty.species.Species
"""
