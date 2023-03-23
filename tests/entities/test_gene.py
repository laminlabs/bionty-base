import pandas as pd

import bionty as bt


def test_ensemble_gene_curation_hgnc_id():
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

    curated_df = bt.Gene(database="ensembl", version="release-108").curate(
        df, reference_id=bt.lookup.gene_id.hgnc_id, column="hgnc id"
    )

    curation = curated_df["__curated__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, True, False])

    assert curation.equals(expected_series)
