import pandas as pd

from bionty import Gene


def test_curate():
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
    df_orig = pd.DataFrame(data).set_index("ensembl_gene_id")
    df_orig.index.name = None

    curated_df = Gene().curate(df_orig)
    assert "orig_index" in curated_df.columns
