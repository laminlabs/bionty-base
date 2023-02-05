from typing import Optional

import pandas as pd
from cached_property import cached_property

from .._normalize import GENE_COLUMNS, NormalizeColumns
from .._settings import s3_bionty_assets
from .._table import EntityTable

ALIAS_DICT = {"symbol": "synonyms"}
FILENAMES = {
    "human": "KJ1HgB695AqbVWvfit8sl.parquet",
    "mouse": "xaBDkhBYLXWHq6gJYnedD.parquet",
}


class Gene(EntityTable):
    """Gene.

    The default indexer is `ensembl_gene_id`

    Args:
        species: `name` of `Species` entity EntityTable.
        id: default is `ensembl_gene_id`

    Notes:
        Biotypes: https://www.ensembl.org/info/genome/genebuild/biotypes.html
        Gene Naming: https://www.ensembl.org/info/genome/genebuild/gene_names.html

    """

    def __init__(
        self,
        species: str = "human",
        id: Optional[str] = None,
        database: Optional[str] = None,
        version: Optional[str] = None,
    ):
        super().__init__(id=id, database=database, version=version)
        if FILENAMES.get(species) is None:
            raise NotImplementedError
        self._species = species
        self._id_field = "ensembl_gene_id" if id is None else id
        self._lookup_col = "symbol"

    @property
    def species(self):
        """The `name` of `Species` entity EntityTable."""
        return self._species

    @cached_property
    def df(self):
        """DataFrame.

        See ingestion: https://lamin.ai/docs/bionty-assets/ingest/ensembl-gene
        """
        cloudpath = s3_bionty_assets(FILENAMES.get(self.species))
        self._filepath = cloudpath.fspath

        df = pd.read_parquet(self._filepath)
        NormalizeColumns.gene(df, species=self.species)
        if not df.index.is_numeric():
            df = df.reset_index().copy()
        df = df[~df[self._id_field].isnull()]
        return df.set_index(self._id_field)

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

        In addition to the .curate() in base class, this also performs alias mapping.
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
            ._curate(df=df, column=column, agg_col=agg_col)
            .rename(columns={column: orig_column})
        )
