import pytest

import bionty as bt


@pytest.fixture(scope="session")
def genes():
    gene_symbols = ["A1CF", "A1BG", "FANCD1", "FANCD20"]
    gn = bt.Gene(source="ensembl", version="release-108")

    return gene_symbols, gn


@pytest.fixture(scope="session")
def celltypes():
    cell_types = ["T-cell", "T cell"]
    ct = bt.CellType(source="cl", version="2023-02-15")

    return cell_types, ct


def test_map_synonyms_mapper(genes):
    gene_symbols, gn = genes

    mapping = gn.map_synonyms(gene_symbols, gn.symbol, return_mapper=True)

    expected_synonym_mapping = {"FANCD1": "BRCA2"}

    assert mapping == expected_synonym_mapping


def test_map_synonyms(genes, celltypes):
    gene_symbols, gn = genes

    mapping = gn.map_synonyms(gene_symbols, gn.symbol, return_mapper=False)
    expected_synonym_mapping = ["A1CF", "A1BG", "BRCA2", "FANCD20"]
    assert mapping == expected_synonym_mapping

    cell_types, ct = celltypes
    mapping = ct.map_synonyms(
        cell_types, ct.name, synonyms_field=ct.synonyms, return_mapper=False
    )
    expected_synonym_mapping = ["T cell", "T cell"]
    assert mapping == expected_synonym_mapping


def test_unsupported_entity():
    bfxp = bt.BFXPipeline()

    with pytest.raises(KeyError):
        bfxp.map_synonyms([], bfxp.name, return_mapper=False)
