from typing import Optional, Literal
import pandas as pd
from .._settings import settings

_IDs = Optional[Literal["ensembl_gene_id", "entrez_id", "uniprot_ids", "hgnc_id"]]
_HGNC = "http://ftp.ebi.ac.uk/pub/databases/genenames/hgnc/tsv/hgnc_complete_set.txt"


class Gene:
    def __init__(self) -> None:
        pass

    def HGNC(self):
        """HGNC symbol from the HUGO Gene Nomenclature Committee"""
        filepath = settings.datasetdir / "hgnc_complete_set.txt"
        filepath.parent.mkdir(exist_ok=True)
        if not filepath.exists():
            from urllib.request import urlretrieve

            urlretrieve(_HGNC, filepath)
        self._hgnc = pd.read_csv(
            filepath,
            sep="\t",
            index_col=0,
            low_memory=False,  # If True, gets DtypeWarning
            verbose=False,
        )
