import pytest

from bionty import CellMarker, Gene, Protein
from bionty._table import EntityTable, _camel_to_snake


def test_entity_table():
    entity_table = EntityTable()
    with pytest.raises(NotImplementedError):
        entity_table.df
    assert entity_table.entity == "entity_table"
    assert _camel_to_snake("EntityTable") == "entity_table"


def species_not_implemented():
    with pytest.raises(NotImplementedError):
        CellMarker(species="mouse")
    with pytest.raises(NotImplementedError):
        Protein(species="cat")
    with pytest.raises(NotImplementedError):
        Gene(species="cat")
