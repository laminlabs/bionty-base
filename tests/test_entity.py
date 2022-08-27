import pytest

from bionty import CellMarker, EntityTable, Protein


def test_entity_table():
    entity_table = EntityTable()
    with pytest.raises(NotImplementedError):
        entity_table.df
    with pytest.raises(NotImplementedError):
        entity_table.ontology


def test_cell_marker():
    with pytest.raises(NotImplementedError):
        CellMarker(species="mouse")
    cell_marker = CellMarker()
    assert cell_marker.entity == "cell_marker"


def test_protein():
    with pytest.raises(NotImplementedError):
        Protein(species="cat")
    protein = Protein()
    assert protein.entity == "protein"
