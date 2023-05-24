import pytest as pytest

import bionty as bt


@pytest.fixture(scope="session")
def genes():
    gene_symbols = ["A1CF", "A1BG", "FANCD1", "FANCD20"]
    gn = bt.Gene(source="ensembl", version="release-108")

    return gene_symbols, gn


def test_map_synonyms_mapper(genes):
    gene_symbols, gn = genes

    mapping = gn.map_synonyms(gene_symbols, gn.symbol, return_mapper=True)

    expected_synonym_mapping = {"FANCD1": "BRCA2"}

    assert mapping == expected_synonym_mapping


def test_map_synonyms(genes):
    gene_symbols, gn = genes

    mapping = gn.map_synonyms(gene_symbols, gn.symbol, return_mapper=False)

    expected_synonym_mapping = ["A1CF", "A1BG", "BRCA2", "FANCD20"]

    assert mapping == expected_synonym_mapping


def test_unsupported_reference_id(genes):
    gene_symbols, gn = genes

    with pytest.raises(ValueError):
        gn.map_synonyms(gene_symbols, gn.ensembl_gene_id, return_mapper=False)


def test_unsupported_bionty():
    bfxp = bt.BFXPipeline()

    with pytest.raises(NotImplementedError):
        bfxp.map_synonyms([], bfxp.name, return_mapper=False)
