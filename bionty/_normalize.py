import pandas as pd

GENE_COLUMNS = {
    "Gene stable ID": "ensembl_gene_id",
    "Transcript stable ID": "ensembl_transcript_id",
    "Protein stable ID": "ensembl_protein_id",
    "Gene name": "gene_symbol",
    "Gene type": "gene_type",
    "NCBI gene (formerly Entrezgene) ID": "ncbi_gene_id",
    "HGNC ID": "hgnc_id",
    "MIM gene accession": "omim_id",
    "Gene Synonym": "gene_synonyms",
    "MGI ID": "mgi_id",
}


class NormalizeColumns:
    """Standardizing column names."""

    def __init__(self) -> None:
        pass

    @staticmethod
    def gene(df: pd.DataFrame, species=None):
        """Column names of gene EntityTables."""
        df.rename(columns=GENE_COLUMNS, inplace=True)
