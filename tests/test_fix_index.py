import pandas as pd

from bionty.dev import explode_aggregated_column_to_expand

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

df = pd.DataFrame(
    {
        "gene symbol": ["corrupted"],
        "hgnc id": ["corrupted"],
        "ensembl_gene_id": ["corrupted1"],
    },
    index=["id"],
)


def test_explode_aggregated_column_to_expand():
    assert "index" in explode_aggregated_column_to_expand(
        df, aggregated_col="ensembl_gene_id"
    )
    df.index.name = "x"
    assert "x" in explode_aggregated_column_to_expand(
        df, aggregated_col="ensembl_gene_id"
    )
