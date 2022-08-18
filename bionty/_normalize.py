import pandas as pd

GENE_COLUMNS = {
    "Gene stable ID": "ensembl_gene_id",
    "Transcript stable ID": "ensembl_transcript_id",
    "Protein stable ID": "ensembl_protein_id",
    "Gene name": "name",
    "Gene type": "gene_type",
    "NCBI gene (formerly Entrezgene) ID": "ncbi_gene_id",
    "HGNC ID": "hgnc_id",
    "MIM gene accession": "omim_id",
    "Gene Synonym": "synonyms",
    "MGI ID": "mgi_id",
}


class NormalizeColumns:
    """Standardizing column names."""

    def __init__(self) -> None:
        pass

    @staticmethod
    def gene(df: pd.DataFrame, species=None):
        """Column names of gene EntityTables.

        We try to adapt a naming system that is {database}.{id_type} when
        multipleids exist within that database.
        - e.g. hgnc_id is the only id in HGNC, therefore it's not using the .
        - e.g. ensembl can have ensembl.gene_id and ensembl.transcript_id
        """
        df.rename(columns=GENE_COLUMNS, inplace=True)
