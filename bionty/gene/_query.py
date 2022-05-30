import io
from typing import Iterable

import pandas as pd
from biothings_client import get_client

from .._normalize import NormalizeColumns


class Mygene:
    """Wrapper of MyGene.info.

    See: https://docs.mygene.info/en/latest/index.html
    """

    def __init__(self) -> None:
        self._server = get_client("gene")

    @property
    def server(self):
        """MyGene.info."""
        return self._server

    def query(
        self,
        genes: Iterable[str],
        scopes="symbol",
        fields="HGNC,symbol",
        species="human",
        as_dataframe=True,
        verbose=False,
        **kwargs,
    ):
        """Get HGNC IDs from Mygene.

        Args:
            genes: Input list
            scopes: ID types of the input
            fields: ID type of the output
            species: species
            as_dataframe: Whether to return a data frame
            verbose: Whether to print logging
            **kwargs: see **kwargs of `biothings_client.MyGeneInfo().querymany()`

        Returns:
            a dataframe ('HGNC' column is reformatted to be 'hgnc_id')
        """
        # query via mygene
        res = self.server.querymany(
            qterms=genes,
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
    """Wrapper of Biomart python APIs, good for accessing Ensembl data.

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
        """biomart.BiomartServer."""
        return self._server

    @property
    def databases(self):
        """Listing all databases."""
        return self._server.databases

    @property
    def datasets(self):
        """Listing all datasets."""
        return self._server.datasets

    @property
    def dataset(self):
        """A biomart.BiomartDataset."""
        return self._dataset

    def get_gene_ensembl(
        self,
        species="human",
        attributes=None,
        filters={},
        **kwargs,
    ):
        """Fetch the reference table of gene ensembl from biomart.

        Args:
            species: common name of species
            attributes: gene attributes from gene_ensembl datasets
            filters: see biomart.search()
            **kwargs: see biomart.search()
        """
        # database name
        from bionty.gene import Gene

        gn = Gene(species=species)
        sname = gn.species.search("short_name")
        self._dataset = self.datasets[f"{sname}_gene_ensembl"]

        # default is to get all the attributes
        attributes = gn.fields if attributes is None else attributes

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
