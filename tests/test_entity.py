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


def test_gene():
    with pytest.raises(NotImplementedError):
        Gene(species="cat")
    gene = Gene()
    assert gene.entity == "gene"


def test_cell_type():
    cell_type = CellType()
    assert cell_type.entity == "cell_type"


def test_species():
    species = Species()
    assert species.entity == "species"


def test_tissue():
    tissue = Tissue()
    assert tissue.entity == "tissue"


def test_disease():
    disease = Disease()
    assert disease.entity == "disease"
