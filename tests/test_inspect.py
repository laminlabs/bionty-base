import pandas as pd
import pytest

import bionty as bt


@pytest.fixture(scope="module")
def genes():
    data = {
        "gene symbol": ["A1CF", "A1BG", "FANCD1", "corrupted"],
        "hgnc id": ["HGNC:24086", "HGNC:5", "HGNC:1101", "corrupted"],
        "ensembl_gene_id": [
            "ENSG00000148584",
            "ENSG00000121410",
            "ENSG00000188389",
            "ENSG0000corrupted",
        ],
    }
    df = pd.DataFrame(data).set_index("ensembl_gene_id")

    gn = bt.Gene(source="ensembl", version="release-109")

    return df, gn


def test_inspect_iterable(genes):
    df, gn = genes

    mapping = gn.inspect(df.index, field=gn.ensembl_gene_id)

    expected_mapping = {
        "mapped": ["ENSG00000148584", "ENSG00000121410", "ENSG00000188389"],
        "not_mapped": ["ENSG0000corrupted"],
    }

    assert mapping == expected_mapping


def test_inspect_return_df(genes):
    df, gn = genes

    mapping = gn.inspect(df.index, field=gn.ensembl_gene_id, return_df=True)

    expected_df = pd.DataFrame(
        index=[
            "ENSG00000148584",
            "ENSG00000121410",
            "ENSG00000188389",
            "ENSG0000corrupted",
        ],
        data={
            "__mapped__": [True, True, True, False],
        },
    )

    assert mapping.equals(expected_df)
