import pandas as pd
import pytest

import bionty as bt


@pytest.fixture(scope="session")
def genes():
    data = {
        "gene symbol": ["A1CF", "A1BG", "FANCD1", "corrupted"],
        "hgnc id": ["HGNC:24086", "HGNC:5", "HGNC:1101", "corrupted"],
        "ensembl_gene_id": [
            "ENSG00000148584",
            "ENSG00000121410",
            "ENSG00000188389",
            "corrupted",
        ],
    }
    df = pd.DataFrame(data).set_index("ensembl_gene_id")

    gn = bt.Gene(source="ensembl", version="release-108")

    return df, gn


def test_gene_ensembl_inspect_hgnc_id(genes):
    df, gn = genes

    inspected_df = gn.inspect(df, field=gn.hgnc_id, column="hgnc id")

    inspect = inspected_df["__mapped__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, True, False])

    assert inspect.equals(expected_series)


def test_gene_ensembl_map_synonyms(genes):
    df, gn = genes

    assert gn.map_synonyms(df["gene symbol"], gn.symbol) == [
        "A1CF",
        "A1BG",
        "BRCA2",
        "corrupted",
    ]

    with pytest.raises(KeyError):
        gn.map_synonyms(df["gene symbol"], gn.symbol, synonyms_field="not exist")
