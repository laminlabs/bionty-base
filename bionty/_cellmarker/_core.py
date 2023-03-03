from typing import Optional

import pandas as pd
from cached_property import cached_property

from .._entity import Entity
from .._settings import s3_bionty_assets


class CellMarker(Entity):
    """Cell markers.

    Args:
        species: `name` of `Species` entity Entity.
    """

    def __init__(
        self,
        species: str = "human",
        id: Optional[str] = "name",
        database: Optional[str] = None,
        version: Optional[str] = None,
    ) -> None:
        super().__init__(id=id, database=database, version=version, species=species)

    @cached_property
    def df(self):
        """DataFrame.

        See ingestion: https://lamin.ai/docs/bionty-assets/ingest/cell-marker-human
        """
        cloudpath = s3_bionty_assets(self._cloud_file_path)
        self._filepath = cloudpath.fspath

        df = pd.read_parquet(self._filepath)
        df.rename(columns={"cell_marker": "name"}, inplace=True)
        df["name"] = df["name"].str.upper()
        # TODO: add to bionty-assets
        df = df.drop_duplicates(subset=["name"])
        if not df.index.is_numeric():
            df = df.reset_index().copy()
        df = df[~df[self._id].isnull()]

        return df.set_index(self._id)
