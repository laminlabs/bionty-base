from functools import cached_property

import pandas as pd

from .._settings import s3_bionty_assets
from .._table import EntityTable

SPECIES_FILENAME = "VpdUdouFahpvStwddqTwk.parquet"


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

    @cached_property
    def df(self) -> pd.DataFrame:
        """DataFrame.

        See ingestion: https://lamin.ai/docs/bionty-assets/ingest/ensembl-species
        """
        cloudpath = s3_bionty_assets(SPECIES_FILENAME)
        self._filepath = cloudpath.fspath

        df = pd.read_parquet(self._filepath)
        df.columns = df.columns.str.lower().str.replace(" ", "_")
        if not df.index.is_numeric():
            df = df.reset_index().copy()
        df = df[~df[self._id_field].isnull()]
        df.common_name = df.common_name.str.lower()
        df.scientific_name = df.scientific_name.str.lower()
        return df.set_index(self._id_field)
