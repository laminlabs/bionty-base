import pytest

from bionty import CellMarker, Gene, Protein
from bionty._entity import Entity, _camel_to_snake


def test_entity_table():
    with pytest.raises(AttributeError):
        entity_table = Entity(database="mondo")
        assert entity_table.df is not None
        assert entity_table.entity == "entity_table"
        assert _camel_to_snake("EntityTable") == "entity_table"


def species_not_implemented():
    with pytest.raises(NotImplementedError):
        CellMarker(species="mouse")
    with pytest.raises(NotImplementedError):
        Protein(species="cat")
    with pytest.raises(NotImplementedError):
        Gene(species="cat")
