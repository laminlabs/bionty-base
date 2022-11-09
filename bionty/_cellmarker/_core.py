from functools import cached_property

import pandas as pd

from .._settings import s3_bionty_assets
from .._table import EntityTable

FILENAMES = {
    "human": "GbC3D7dKnsomHB7ZMeUpC.parquet",
}


class CellMarker(EntityTable):
    """Cell markers.

    Args:
        species: `common_name` of `Species` entity EntityTable.
    """

    def __init__(self, species="human", id=None) -> None:
        super().__init__(id=id)
        if FILENAMES.get(species) is None:
            raise NotImplementedError
        self._species = species
        self._id_field = "name" if id is None else id

    @property
    def species(self):
        """The `common_name` of `Species` entity EntityTable."""
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
