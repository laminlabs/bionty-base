from collections import namedtuple
from functools import cached_property

import pandas as pd

from .._fix_index import get_compliant_index_from_column
from .._normalize import NormalizeColumns
from .._settings import check_datasetdir_exists, settings
from .._table import Table

STD_ID_DICT = {"human": "hgnc_symbol", "mouse": "mgi_symbol"}
FILENAMES = {"human": "hgnc_complete_set.feather", "mouse": "mgi_complete_set.feather"}


class Gene(Table):
    """Gene.

    Args:
        species: `common_name` of `Species` entity table.
        id: If `None`, chooses an id field in a species dependent way.

    Notes:
        Biotypes: https://useast.ensembl.org/info/genome/genebuild/biotypes.html
        Gene Naming: https://useast.ensembl.org/info/genome/genebuild/gene_names.html

    """

    def __init__(
        self,
        species="human",
        id=None,
    ):
        self._species = species
        self._filepath = settings.datasetdir / FILENAMES[species]
        self._bionty_id = STD_ID_DICT[species] if id is None else id

    @property
    def species(self):
        """The `common_name` of `Species` entity table."""
        return self._species

    @property
    def filepath(self):
        """The local filepath to the DataFrame."""
        return self._filepath

    @property
    def bionty_id(self):
        """The field of bionty id."""
        return self._bionty_id

    @cached_property
    def df(self):
        """DataFrame."""
        if self.species not in {"human", "mouse"}:
            raise NotImplementedError
        else:
            if not self.filepath.exists():
                self._download_df()
            df = pd.read_feather(self.filepath)
            NormalizeColumns.gene(df, species=self.species)
            if not isinstance(df.index, pd.RangeIndex):
                df = df.reset_index().copy()
            return df.set_index(self.bionty_id)

    @cached_property
    def lookup(self):
        """Lookup object for auto-complete."""
        values = self.df.index.str.replace("-", "_").str.rstrip("@").to_list()
        return namedtuple("id", values)

    def standardize(
        self, df: pd.DataFrame, column: str = None, keep_data=True, **kwargs
    ):
        """Index a dataframe with bionty id."""
        # when query column is the index, pop the original index as a `index_org` column
        if column is None:
            df[self.bionty_id] = df.index
            column = self.bionty_id

        compliant_index, _ = get_compliant_index_from_column(
            df=df,
            ref_df=self.df,
            column=column,
            keep_data=keep_data,
        )

        df.index = compliant_index
        df.index.name = self.bionty_id
        df.rename(columns={self.bionty_id: "index_orig"}, inplace=True)
        if not keep_data:
            return df[~df.index.isnull()]

    @check_datasetdir_exists
    def _download_df(self):
        from urllib.request import urlretrieve

        urlretrieve(
            f"https://bionty-assets.s3.amazonaws.com/{FILENAMES[self.species]}",
            self.filepath,
        )
