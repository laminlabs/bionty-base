from typing import Optional

import pandas as pd
from cached_property import cached_property

from .._settings import s3_bionty_assets
from .._table import EntityTable

FILENAMES = {
    "human": "GbC3D7dKnsomHB7ZMeUpC.parquet",
}


class CellMarker(EntityTable):
    """Cell markers.

    Args:
        species: `name` of `Species` entity EntityTable.
    """

    def __init__(
        self,
        species: str = "human",
        id: Optional[str] = None,
        database: Optional[str] = None,
        version: Optional[str] = None,
    ) -> None:
        super().__init__(id=id, database=database, version=version)
        if FILENAMES.get(species) is None:
            raise NotImplementedError
        self._species = species
        self._id_field = "name" if id is None else id

    @property
    def species(self):
        """The `name` of `Species` entity EntityTable."""
        return self._species

    @cached_property
    def df(self):
        """DataFrame.

        See ingestion: https://lamin.ai/docs/bionty-assets/ingest/cell-marker-human
        """
        cloudpath = s3_bionty_assets(FILENAMES.get(self.species))
        self._filepath = cloudpath.fspath

        df = pd.read_parquet(self._filepath)
        df.rename(columns={"cell_marker": "name"}, inplace=True)
        df["name"] = df["name"].str.upper()
        # TODO: add to bionty-assets
        df = df.drop_duplicates(subset=["name"])
        if not df.index.is_numeric():
            df = df.reset_index().copy()
        df = df[~df[self._id_field].isnull()]
        return df.set_index(self._id_field)
