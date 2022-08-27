import pandas as pd
import pytest

from bionty.dev import (
    explode_aggregated_column_to_expand,
    get_compliant_index_from_column,
)

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
    }
)


def test_get_compliant_index_from_column():
    with pytest.raises(AssertionError):
        get_compliant_index_from_column(df, ref_df=df_orig, column="x")
    with pytest.raises(AssertionError):
        get_compliant_index_from_column(df, ref_df=df_orig, column="ensembl_gene_id")


def test_explode_aggregated_column_to_expand():
    assert "index" in explode_aggregated_column_to_expand(
        df, aggregated_col="ensembl_gene_id"
    )
    df.index.name = "x"
    assert "x" in explode_aggregated_column_to_expand(
        df, aggregated_col="ensembl_gene_id"
    )
