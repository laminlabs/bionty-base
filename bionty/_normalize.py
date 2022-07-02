import pandas as pd

GENE_COLUMNS = {
    "HGNC": "hgnc_id",
    "ensembl_gn_id": "ensembl.gene_id",
    "ensembl_gene_id": "ensembl.gene_id",
    "entrezgene_id": "entrez.gene_id",
    "entrez_id": "entrez.gene_id",
    "MGI Marker Accession ID": "mgi_id",
    "Marker Symbol": "mgi_symbol",
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
        if species == "human":
            GENE_COLUMNS.update({"symbol": "hgnc_symbol"})
        df.rename(columns=GENE_COLUMNS, inplace=True)
