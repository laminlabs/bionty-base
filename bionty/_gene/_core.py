from collections import namedtuple
from functools import cached_property

import pandas as pd

from .._normalize import GENE_COLUMNS, NormalizeColumns
from .._settings import check_datasetdir_exists, settings
from .._table import EntityTable

STD_ID_DICT = {"human": "hgnc_symbol", "mouse": "mgi_symbol"}
FILENAMES = {"human": "hgnc_complete_set.feather", "mouse": "mgi_complete_set.feather"}
ALIAS_DICT = {"hgnc_symbol": "alias_symbol", "mgi_symbol": "Synonyms"}


class Gene(EntityTable):
    """Gene.

    The default indexes chosen are
    - human: hgnc_symbol
    - mouse: mgi_symbol

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
    def entity(self):
        """Name of the entity."""
        return "gene"

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
        values = {i.replace("-", "_").rstrip("@"): i for i in self.df.index.values}
        nt = namedtuple(self._id_field, values.keys())

        return nt(**values)

    @check_datasetdir_exists
    def _download_df(self):
        from urllib.request import urlretrieve

        urlretrieve(
            f"https://bionty-assets.s3.amazonaws.com/{FILENAMES[self.species]}",
            self._filepath,
        )

    def curate(  # type: ignore
        self, df: pd.DataFrame, column: str = None
    ) -> pd.DataFrame:
        """Curate index of passed DataFrame to conform with default identifier.

        - If `column` is `None`, checks the existing index for compliance with
          the default identifier.
        - If `column` denotes an entity identifier, tries to map that identifier
          to the default identifier.

        Returns the DataFrame with the curated index and a boolean `__curated__`
        column that indicates compliance with the default identifier.
        """
        agg_col = ALIAS_DICT.get(self._id_field)
        df = df.copy()

        # if the query column name does not match any columns in the self.df
        # Bionty assume the query column and the self._id_field uses the same type of
        # identifier
        orig_column = column
        if column is not None and column not in self.df.columns:
            # normalize the identifier column
            column_norm = GENE_COLUMNS.get(column)
            if column_norm in df.columns:
                raise ValueError("{column_norm} column already exist!")
            else:
                column = self._id_field if column_norm is None else column_norm
                df.rename(columns={orig_column: column}, inplace=True)
            agg_col = ALIAS_DICT.get(column)
        return (
            super()
            .curate(df=df, column=column, agg_col=agg_col)
            .rename(columns={column: orig_column})
        )
