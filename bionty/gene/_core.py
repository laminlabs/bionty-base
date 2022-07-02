from collections import namedtuple
from functools import cached_property

import pandas as pd

from .._normalize import NormalizeColumns
from .._settings import check_datasetdir_exists, settings
from .._table import EntityTable

STD_ID_DICT = {"human": "hgnc_symbol", "mouse": "mgi_symbol"}
FILENAMES = {"human": "hgnc_complete_set.feather", "mouse": "mgi_complete_set.feather"}


class Gene(EntityTable):
    """Gene.

    The default indexes chosen are
    - human: HGNC symbol
    - mouse: MGI symbol

    We think these identifiers are the best unambiguous ways to reference genes.

    Args:
        species: `common_name` of `Species` entity EntityTable.
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
        self._id_field = STD_ID_DICT[species] if id is None else id

    @property
    def species(self):
        """The `common_name` of `Species` entity EntityTable."""
        return self._species

    @cached_property
    def df(self):
        """DataFrame."""
        if self.species not in {"human", "mouse"}:
            raise NotImplementedError
        else:
            if not self._filepath.exists():
                self._download_df()
            df = pd.read_feather(self._filepath)
            NormalizeColumns.gene(df, species=self.species)
            if not isinstance(df.index, pd.RangeIndex):
                df = df.reset_index().copy()
            return df.set_index(self._id_field)

    @cached_property
    def lookup(self):
        """Lookup object for auto-complete."""
        values = self.df.index.str.replace("-", "_").str.rstrip("@").to_list()
        return namedtuple("id", values)

    @check_datasetdir_exists
    def _download_df(self):
        from urllib.request import urlretrieve

        urlretrieve(
            f"https://bionty-assets.s3.amazonaws.com/{FILENAMES[self.species]}",
            self._filepath,
        )
