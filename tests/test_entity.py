import pytest

from bionty import (
    CellMarker,
    CellType,
    Disease,
    EntityTable,
    Gene,
    Protein,
    Species,
    Tissue,
)


def test_entity_table():
    entity_table = EntityTable()
    with pytest.raises(NotImplementedError):
        entity_table.df
    with pytest.raises(NotImplementedError):
        entity_table.ontology


def species_not_implemented():
    with pytest.raises(NotImplementedError):
        CellMarker(species="mouse")
    with pytest.raises(NotImplementedError):
        Protein(species="cat")
    with pytest.raises(NotImplementedError):
        Gene(species="cat")


def test_entity():
    assert Gene().entity == "gene"
    assert Protein().entity == "protein"
    assert CellMarker().entity == "cell_marker"
    assert Species().entity == "species"
    assert Tissue().entity == "tissue"
    assert CellType().entity == "cell_type"
    assert Disease().entity == "disease"
