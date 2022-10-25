from functools import cached_property

import pandas as pd

from .._settings import check_datasetdir_exists, settings
from .._table import EntityTable

SPECIES_FILENAME = (
    "https://bionty-assets.s3.amazonaws.com/VpdUdouFahpvStwddqTwk.parquet"
)


class Species(EntityTable):
    """Species.

    Args:
        id: Field name that should constitute the primary reference for each
            value. It will also be the primary key in the corresponding SQL EntityTable.
    """

    def __init__(self, id=None):
        super().__init__(id=id)
        self._id_field = "common_name" if id is None else id
        self._lookup_col = "common_name"
        self._filepath = settings.datasetdir / SPECIES_FILENAME.split("/")[-1]

    @cached_property
    def df(self) -> pd.DataFrame:
        """DataFrame.

        See ingestion: https://lamin.ai/docs/bionty-assets/ingest/ensembl-species
        """
        df = pd.read_parquet(SPECIES_FILENAME)
        df.columns = df.columns.str.lower().str.replace(" ", "_")
        if not df.index.is_numeric():
            df = df.reset_index().copy()
        df = df[~df[self._id_field].isnull()]
        df.common_name = df.common_name.str.lower()
        df.scientific_name = df.scientific_name.str.lower()
        return df.set_index(self._id_field)

    @check_datasetdir_exists
    def _download_df(self):
        from urllib.request import urlretrieve

        urlretrieve(
            SPECIES_FILENAME,
            self._filepath,
        )
