from typing import Literal, Optional

import pandas as pd

from .._bionty import Bionty
from .._normalize import NormalizeColumns
from ..dev._io import s3_bionty_assets
from ._shared_docstrings import _doc_params, doc_entites


@_doc_params(doc_entities=doc_entites)
class Gene(Bionty):
    """Gene.

    1. Ensembl
    Edits of terms are coordinated and reviewed on:
    https://www.ensembl.org/

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
            **kwargs,
        )

    def df(self) -> pd.DataFrame:
        """DataFrame.

        The default indexer is `ensembl_gene_id`

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
        df = df[~df["ensembl_gene_id"].isnull()]

        return df

    def lookup(self, field: str = "symbol") -> tuple:
        """Return an auto-complete object for the bionty field.

        Args:
            field: The field to lookup the values for.
                   Defaults to 'name'.

        Returns:
            A NamedTuple of lookup information of the field values.

        Examples:
            >>> import bionty as bt
            >>> gene_lookout = bt.Gene().lookup()
            >>> gene_lookout.TEF
        """
        return super().lookup(field=field)
