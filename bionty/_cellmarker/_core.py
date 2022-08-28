from collections import namedtuple
from functools import cached_property

import pandas as pd

from .._settings import check_datasetdir_exists, settings
from .._table import EntityTable, _todict


class CellMarker(EntityTable):
    """Cell markers.

    Args:
        species: `common_name` of `Species` entity EntityTable.
    """

    def __init__(self, species="human", id=None) -> None:
        super().__init__(id=id)
        if species not in {"human"}:
            raise NotImplementedError
        self._species = species
        self._filepath = settings.datasetdir / f"CellMarker-{self.species}.feather"
        self._id_field = "cell_marker" if id is None else id

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
        df = pd.read_feather(self._filepath)
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
            f"https://bionty-assets.s3.amazonaws.com/CellMarker-{self.species}.feather",
            self._filepath,
        )
