from typing import Iterable
import io
import pandas as pd
from biothings_client import MyGeneInfo
from .. import NormalizeColumns


class Mygene(MyGeneInfo):
    """Wrapper of MyGene.info

    See: https://docs.mygene.info/en/latest/index.html
    """

    def __init__(self) -> None:
        super().__init__()

    def querymany(
        self,
        genes: Iterable[str],
        scopes="symbol",
        fields="HGNC,symbol",
        species="human",
        as_dataframe=True,
        verbose=False,
        **kwargs,
    ):
        """Get HGNC IDs from Mygene

        Parameters
        ----------
        genes
            Input list
        scopes
            ID types of the input
        fields
            ID type of the output
        **kwargs
            see **kwargs of `biothings_client.MyGeneInfo().querymany()`

        Returns
        -------
        a dataframe ('HGNC' column is reformatted to be 'hgnc_id')
        """

        # query via mygene
        res = super().querymany(
            genes,
            scopes=scopes,
            fields=fields,
            species=species,
            as_dataframe=as_dataframe,
            verbose=verbose,
            **kwargs,
        )

        # format HGNC IDs to match `hgnc_id` format ('HGNC:int')
        if "HGNC" in res.columns:
            res["HGNC"] = [
                f"HGNC:{i}" if isinstance(i, str) else i for i in res["HGNC"]
            ]
        NormalizeColumns.gene(res)

        return res


class Biomart:
    """Wrapper of Biomart python APIs, good for accessing Ensembl data

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
        attributes=None,
        filters={},
        **kwargs,
    ):
        """Fetch the reference table of gene ensembl from biomart

        Parameters
        ----------
        species
            common name of species
        attributes
            gene attributes from gene_ensembl datasets
        filters
            see biomart.search()
        **kwargs
            see biomart.search()
        """
        # database name
        from bionty.gene import Gene

        gn = Gene(species=species)
        sname = gn.species.get_attribute("short_name")
        self._dataset = self.datasets[f"{sname}_gene_ensembl"]

        # default is to get all the attributes
        attributes = gn.attributes if attributes is None else attributes

        # Get the mapping between the attributes
        response = self.dataset.search(
            {"filters": filters, "attributes": attributes},
            **kwargs,
        )
        data = response.raw.data.decode("utf-8")

        # returns a dataframe
        df = pd.read_csv(io.StringIO(data), sep="\t", header=None)
        df.columns = attributes

        return df
