from collections import namedtuple
from functools import cached_property
from typing import Literal

import pandas as pd

from .._normalize import NormalizeColumns
from .._settings import check_datasetdir_exists, settings
from .._table import Table

_IDs = Literal["ensembl.gene_id", "entrez.gene_id"]


STD_ID_DICT = {"human": "hgnc_symbol", "mouse": "mgi_symbol"}
ATTR_DICT = {"human": ["hgnc_id", "hgnc_symbol"], "mouse": ["mgi_symbol"]}
FILENAMES = {"human": "hgnc_complete_set.feather", "mouse": "mgi_complete_set.feather"}


class Gene(Table):
    """Gene.

    Args:
        id: If `None`, chooses an id field in a species dependent way.
        species: `common_name` of `Species` entity table.

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
        self._id_field = STD_ID_DICT[species]
        self._filepath = settings.datasetdir / FILENAMES[species]

    @property
    def species(self):
        """The `common_name` of `Species` entity table."""
        return self._species

    @property
    def filepath(self):
        """The local filepath to the DataFrame."""
        return self._filepath

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
            self.filepath,
        )
