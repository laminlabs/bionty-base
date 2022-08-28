import pandas as pd

from bionty import Gene, Protein


def test_gene_curate():
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


def test_protein_curate():
    data = {"uniprot id": ["O00444", "O00453", "corrupted"]}
    df_orig = pd.DataFrame(data).set_index("uniprot id")

    curated_df = Protein().curate(df_orig)
    assert curated_df["__curated__"].tolist() == [True, True, False]
