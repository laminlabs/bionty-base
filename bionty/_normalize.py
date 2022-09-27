import pandas as pd

GENE_COLUMNS = {
    "Gene stable ID": "ensembl_gene_id",
    "Transcript stable ID": "ensembl_transcript_id",
    "Protein stable ID": "ensembl_protein_id",
    "Gene name": "symbol",
    "Gene type": "gene_type",
    "Gene description": "description",
    "NCBI gene (formerly Entrezgene) ID": "ncbi_gene_id",
    "HGNC ID": "hgnc_id",
    "MIM gene accession": "omim_id",
    "Gene Synonym": "synonyms",
    "MGI ID": "mgi_id",
}

PROTEIN_COLUMNS = {
    "Entry": "uniprotkb_id",
    "Entry Name": "uniprotkb_name",
    "Protein names": "synonyms",
    "Length": "length",
    "Organism (ID)": "species_id",
    "Gene Names (primary)": "gene_symbols",
    "Gene Names (synonym)": "gene_synonyms",
    "Ensembl": "ensembl_transcript_ids",
    "GeneID": "ncbi_gene_ids",
}


class NormalizeColumns:
    """Standardizing column names."""

    @staticmethod
    def gene(df: pd.DataFrame, species=None):
        """Column names of gene EntityTables."""
        df.rename(columns=GENE_COLUMNS, inplace=True)

    @staticmethod
    def protein(df: pd.DataFrame, species=None):
        """Column names of protein EntityTables."""
        df.rename(columns=PROTEIN_COLUMNS, inplace=True)
