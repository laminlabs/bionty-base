import pytest

from bionty import CellMarker, EntityTable, Gene, Protein


def test_entity_table():
    entity_table = EntityTable()
    with pytest.raises(NotImplementedError):
        entity_table.df
    with pytest.raises(NotImplementedError):
        entity_table.ontology
    assert entity_table.entity == "entity_table"


def species_not_implemented():
    with pytest.raises(NotImplementedError):
        CellMarker(species="mouse")
    with pytest.raises(NotImplementedError):
        Protein(species="cat")
    with pytest.raises(NotImplementedError):
        Gene(species="cat")
