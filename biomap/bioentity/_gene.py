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


class Biomart:
    """Wrapper of Biomart APIs

    See: https://github.com/sebriois/biomart
    """

    def __init__(self) -> None:
        try:
            import biomart

            self._server = biomart.BiomartServer("http://uswest.ensembl.org/biomart")
            self._dataset = None
        except ModuleNotFoundError:
            raise ModuleNotFoundError("Run `pip install biomart`")

    @property
    def server(self):
        """biomart.BiomartServer"""
        return self._server

    @property
    def databases(self):
        """Listing all databases"""
        return self._server.databases

    @property
    def datasets(self):
        """Listing all datasets"""
        return self._server.datasets

    @property
    def dataset(self):
        """A biomart.BiomartDataset"""
        return self._dataset

    def get_gene_ensembl(
        self,
        species="human",
        attributes=["ensembl_gene_id", "hgnc_id", "hgnc_symbol"],
        filters={},
        **kwargs,
    ):
        # database name
        sname = Species.get_attribute("short_name")[species]
        self._dataset = self.datasets[f"{sname}_gene_ensembl"]

        # Get the mapping between the attributes
        response = self.dataset.search(
            {"filters": filters, "attributes": attributes}, **kwargs
        )
        data = response.raw.data.decode("utf-8")

        # returns a dataframe
        df = pd.read_csv(io.StringIO(data), sep="\t", header=None)
        df.columns = attributes

        return df
