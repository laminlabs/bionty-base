import pandas as pd
import pytest

import bionty as bt


@pytest.fixture(scope="session")
def genes():
    gene_ids = [
        "ENSG00000148584",
        "ENSG00000121410",
        "ENSG00000188389",
        "ENSG0000corrupted",
    ]
    gn = bt.Gene(source="ensembl", version="release-108")

    return gene_ids, gn


def test_inspect_iterable(genes):
    gene_ids, gn = genes

    mapping = gn.inspect(gene_ids, reference_id=gn.ensembl_gene_id)

    expected_mapping = {
        "mapped": ["ENSG00000148584", "ENSG00000121410", "ENSG00000188389"],
        "not_mapped": ["ENSG0000corrupted"],
    }

    assert mapping == expected_mapping


def test_inspect_return_df(genes):
    gene_ids, gn = genes

    mapping = gn.inspect(gene_ids, reference_id=gn.ensembl_gene_id, return_df=True)

    expected_df = pd.DataFrame(
        data={
            "ensembl_gene_id": [
                "ENSG00000148584",
                "ENSG00000121410",
                "ENSG00000188389",
                "ENSG0000corrupted",
            ],
            "__mapped__": [True, True, True, False],
        }
    )

    assert mapping.equals(expected_df)  # type: ignore
