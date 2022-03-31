from typing import Optional, Literal
import pandas as pd
from .._settings import settings

_IDs = Optional[Literal["ensembl_gene_id", "entrez_id", "uniprot_ids", "hgnc_id"]]
_HGNC = "http://ftp.ebi.ac.uk/pub/databases/genenames/hgnc/tsv/hgnc_complete_set.txt"


class Gene:
    """Gene

    Biotypes: https://useast.ensembl.org/info/genome/genebuild/biotypes.html
    Gene Naming: https://useast.ensembl.org/info/genome/genebuild/gene_names.html

    """

    def __init__(self) -> None:
        pass

    @classmethod
    def attributes(cls, species="human"):
        shared = [
            "ensembl_gene_id",
            "entrezgene_id",
            "uniprot_gn_id",
        ]
        attr_dict = {"human": ["hgnc_id", "hgnc_symbol"], "mouse": ["mgi_symbol"]}
        return shared + attr_dict[species]

    @classmethod
    def HGNC(cls, species="human"):
        """HGNC symbol from the HUGO Gene Nomenclature Committee"""
        if species != "human":
            raise AssertionError("HGNC is only for human!")

        filepath = settings.datasetdir / "hgnc_complete_set.txt"
        filepath.parent.mkdir(exist_ok=True)
        if not filepath.exists():
            from urllib.request import urlretrieve

            urlretrieve(_HGNC, filepath)
        return pd.read_csv(
            filepath,
            sep="\t",
            index_col=0,
            low_memory=False,  # If True, gets DtypeWarning
            verbose=False,
        )
