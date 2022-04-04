from typing import Optional, Literal
import io
import pandas as pd
from ._species import Species
from .._settings import settings

_IDs = Optional[Literal["ensembl_gene_id", "entrezgene_id", "uniprot_gn_id"]]
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
    def get_gene_ensembl(
        cls, species="human", attributes=["ensembl_gene_id", "hgnc_id", "hgnc_symbol"]
    ):
        # Set up connection to server
        import biomart

        server = biomart.BiomartServer("http://uswest.ensembl.org/biomart")

        sname = Species.get_attribute("short_name")[species]
        mart = server.datasets[f"{sname}_gene_ensembl"]

        # Get the mapping between the attributes
        response = mart.search({"attributes": attributes})
        data = response.raw.data.decode("ascii")

        df = pd.read_csv(io.StringIO(data), sep="\t", header=None)
        df.columns = attributes

        return df

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
