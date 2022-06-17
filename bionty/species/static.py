from typing import Any, NamedTuple

from .._models import Entity, create_model
from .object import Species


def create_species_model(std_id="scientific_name", **kwargs):
    """Create the species data model with pydantic.

    Args:
        std_id: the field used as standardized id
        **kwargs: see `_models.create_model`

    Returns:
        `SpeciesData` data model with each species as a namedtuple entry
    """
    model = create_model("SpeciesData", __base__=Entity, **kwargs)
    df = Species().df.reset_index()
    for i in df.index:
        entry = {}
        entry.update({col: df.loc[i][col] for col in df.columns})
        model.add_fields(**{df.loc[i][std_id]: (Entry, Entry(**entry))})
    return model


class Entry(NamedTuple):
    display_name: str
    scientific_name: str
    common_name: str
    taxon_id: int
    assembly: str
    accession: str
    release: int
    short_name: str


SpeciesDataModel: Any = create_species_model()


class SpeciesModel(SpeciesDataModel):
    def __call__(self, **kwargs):
        return Species(**kwargs)


species = SpeciesModel(**{"name": "species", "std_id": "scientific_name"})
"""Access point to species.

`species` -> a static class containing species as fields
`species()` -> an instance of bionty.species.Species
"""
