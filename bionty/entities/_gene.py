from typing import Literal, Optional, Union

import pandas as pd

from .._entity import Bionty, BiontyField
from .._normalize import GENE_COLUMNS, NormalizeColumns
from ..dev._io import s3_bionty_assets
from ._shared_docstrings import _doc_params, doc_curate, doc_entites


@_doc_params(doc_entities=doc_entites)
class Gene(Bionty):
    """Gene.

    1. Ensembl
    Edits of terms are coordinated and reviewed on:
    https://www.ensembl.org/

    The default indexer is `ensembl_gene_id`

    Args:
        {doc_entities}

    Notes:
        Biotypes: https://www.ensembl.org/info/genome/genebuild/biotypes.html
        Gene Naming: https://www.ensembl.org/info/genome/genebuild/gene_names.html
    """

    def __init__(
        self,
        species: str = "human",
        source: Optional[Literal["ensembl"]] = None,
        version: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(
            source=source,
            version=version,
            species=species,
            reference_id="ensembl_gene_id",
            **kwargs,
        )
        self._lookup_field = "symbol"
        self._synonyms_dict = {"symbol": "synonyms"}

    def df(self) -> pd.DataFrame:
        """DataFrame.

        See ingestion: https://lamin.ai/docs/bionty-assets/ingest/ensembl-gene
        """
        self._filepath = s3_bionty_assets(self._parquet_filename)

        df = pd.read_parquet(self._filepath)
        NormalizeColumns.gene(df, species=self.species)
        try:
            # for pandas > 2.0
            if not pd.api.types.is_any_real_numeric_dtype(df.index):
                df = df.reset_index().copy()
        except AttributeError:
            if not df.index.is_numeric():
                df = df.reset_index().copy()
        df = df[~df[self.reference_id].isnull()]

        return df

    @_doc_params(doc_curate=doc_curate)
    def curate(  # type: ignore
        self,
        df: pd.DataFrame,
        column: str = None,
        reference_id: Union[BiontyField, str] = "ensembl_gene_id",
    ) -> pd.DataFrame:
        """Curate index of passed DataFrame to conform with default identifier.

        In addition to the .curate() in base class, this also performs alias mapping.

        Args:
            {doc_curate}

        Returns:
            The input DataFrame with the curated index and a boolean `__curated__`
            column that indicates compliance with the default identifier.
        """
        reference_id = str(reference_id)
        agg_col = self._synonyms_dict.get(reference_id)
        df = df.copy()

        # if the query column name does not match any columns in the self.df()
        # Bionty assume the query column and the self.reference_id field use
        # the same type of identifier
        orig_column = column
        if column is not None and column not in self.df().columns:
            # normalize the target column
            column_norm = GENE_COLUMNS.get(column)
            if column_norm in df.columns:
                raise ValueError(f"{column_norm} column already exist!")
            else:
                column = reference_id if column_norm is None else column_norm
                df.rename(columns={orig_column: column}, inplace=True)
            agg_col = self._synonyms_dict.get(column)

        return (
            super()
            ._curate(
                df=df,
                column=column,
                agg_col=agg_col,
                reference_id=reference_id,
            )
            .rename(columns={column: orig_column})
        )

    def lookup(self, field: str = "symbol"):
        return super().lookup(field=field)
