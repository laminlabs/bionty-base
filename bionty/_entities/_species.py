from typing import Optional

import pandas as pd
from cached_property import cached_property

from .._entity import Entity

SPECIES_FILENAME = "VpdUdouFahpvStwddqTwk.parquet"


class Species(Entity):
    """Species.

    Args:
        id: Field name that should constitute the primary reference for each
            value. It will also be the primary key in the corresponding SQL Entity.
    """

    def __init__(
        self,
        id: Optional[str] = None,
        database: Optional[str] = None,
        version: Optional[str] = None,
    ):
        id = "name" if id is None else id
        super().__init__(id=id, database=database, version=version)

    @cached_property
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

        return df.set_index(self._id)