from typing import Literal, Optional

import pandas as pd

from bionty.entities._shared_docstrings import _doc_params, species_removed

from .._entity import Bionty


@_doc_params(doc_entities=species_removed)
class Species(Bionty):
    """Species.

    1. Species ontology
    Edits of terms are coordinated and reviewed on:
    https://www.ensembl.org/index.html

    Args:
        {doc_entities}
    """

    def __init__(
        self,
        source: Optional[Literal["ensembl"]] = None,
        version: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(source=source, version=version, reference_id="name", **kwargs)

    def df(self) -> pd.DataFrame:
        """DataFrame.

        See ingestion: https://lamin.ai/docs/bionty-assets/ingest/ensembl-species
        """
        url = f"https://ftp.ensembl.org/pub/{self._version}/species_EnsemblVertebrates.txt"  # noqa
        self._filepath = self._url_download(url)

        df = pd.read_csv(self._filepath, sep="\t", index_col=False)
        df.rename(
            columns={
                "#name": "name",
                "species": "scientific_name",
                "taxonomy_id": "taxon_id",
            },
            inplace=True,
        )
        df["name"] = df["name"].str.lower()
        df.insert(0, "id", "NCBI_" + df["taxon_id"].astype(str))

        return df
