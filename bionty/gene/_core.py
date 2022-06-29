from collections import namedtuple
from functools import cached_property
from typing import Literal

import pandas as pd

from .._normalize import NormalizeColumns
from .._settings import check_datasetdir_exists, settings
from .._table import Table

_IDs = Literal["ensembl.gene_id", "entrez.gene_id"]
_HGNC = "https://bionty-assets.s3.amazonaws.com/hgnc_complete_set.txt"


STD_ID_DICT = {"human": "hgnc_symbol", "mouse": "mgi_symbol"}
ATTR_DICT = {"human": ["hgnc_id", "hgnc_symbol"], "mouse": ["mgi_symbol"]}


class Gene(Table):
    """Gene.

    Args:
        id: If `None`, chooses an id field in a species dependent way.
        species: `common_name` of `Species` entity table.

    Notes:
        Biotypes: https://useast.ensembl.org/info/genome/genebuild/biotypes.html
        Gene Naming: https://useast.ensembl.org/info/genome/genebuild/gene_names.html

    """

    def __init__(self, id=None, species="human"):
        self._species = species
        self._id_field = STD_ID_DICT[species]

    @property
    def species(self):
        """The `common_name` of `Species` entity table."""
        return self._species

    @cached_property
    def df(self):
        """DataFrame."""
        if self._species == "human":
            return self._hgnc()
        else:
            raise NotImplementedError

    @cached_property
    def lookup(self):
        """Lookup object for auto-complete."""
        values = self.df.index.str.replace("-", "_").str.rstrip("@").to_list()
        return namedtuple("id", values)

    @check_datasetdir_exists
    def _hgnc(self):
        """HGNC symbol from the HUGO Gene Nomenclature Committee."""
        assert self.species == "human"

        filepath = settings.datasetdir / "hgnc_complete_set.txt"
        if not filepath.exists():
            print("retrieving HUGO complete gene set from EBI")
            from urllib.request import urlretrieve

            urlretrieve(_HGNC, filepath)
        df = pd.read_csv(
            filepath,
            sep="\t",
            index_col=0,
            low_memory=False,  # If True, gets DtypeWarning
            verbose=False,
        )
        df = df.reset_index().copy()
        NormalizeColumns.gene(df, species=self.species)

        df = df.set_index("hgnc_symbol")

        return df
