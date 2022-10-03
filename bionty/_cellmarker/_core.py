from collections import namedtuple
from functools import cached_property

import pandas as pd

from .._settings import check_datasetdir_exists, settings
from .._table import EntityTable, _todict

S3_BUCKET = "https://bionty-assets.s3.amazonaws.com"
FILENAMES = {
    "human": "IMqRe61Gvces1wrzKAlzl-1.parquet",
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
        self._filepath = settings.datasetdir / FILENAMES.get(self.species)
        self._id_field = "name" if id is None else id

    @property
    def species(self):
        """The `common_name` of `Species` entity EntityTable."""
        return self._species

    @cached_property
    def df(self):
        """DataFrame.

        See ingestion: https://lamin.ai/docs/bionty-assets/ingest/2022-08-26-cell-marker
        """
        if not self._filepath.exists():
            self._download_df()
        df = pd.read_parquet(self._filepath)
        df.rename(columns={"cell_marker": "name"}, inplace=True)
        df["name"] = df["name"].str.upper()
        # TODO: add to bionty-assets
        df = df.drop_duplicates(subset=["name"])
        if not df.index.is_numeric():
            df = df.reset_index().copy()
        df = df[~df[self._id_field].isnull()]
        return df.set_index(self._id_field)

    @cached_property
    def lookup(self):
        """Lookup object for auto-complete."""
        values = _todict(self.df.index.values)
        nt = namedtuple(self._id_field, values.keys())

        return nt(**values)

    @check_datasetdir_exists
    def _download_df(self):
        from urllib.request import urlretrieve

        urlretrieve(
            f"{S3_BUCKET}/{FILENAMES.get(self.species)}",
            self._filepath,
        )
