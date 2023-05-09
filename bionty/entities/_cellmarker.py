from typing import Literal, Optional

import pandas as pd

from .._entity import Entity
from ..dev._io import s3_bionty_assets
from ._shared_docstrings import _doc_params, doc_curate, doc_entites

ALIAS_DICT = {"name": "synonyms"}


@_doc_params(doc_entities=doc_entites)
class CellMarker(Entity):
    """Cell markers.

    1. Cell Marker Ontology
    Edits of terms are coordinated and reviewed on:
    http://bio-bigdata.hrbmu.edu.cn/CellMarker/

    Args:
        {doc_entities}
    """

    def __init__(
        self,
        species: str = "human",
        source: Optional[Literal["cellmarker"]] = None,
        version: Optional[str] = None,
        **kwargs
    ) -> None:
        super().__init__(
            source=source,
            version=version,
            species=species,
            reference_id="name",
            **kwargs
        )

    def df(self) -> pd.DataFrame:
        """DataFrame.

        See ingestion: https://lamin.ai/docs/bionty-assets/ingest/cell-marker-2.0
        """
        localpath = s3_bionty_assets(self._cloud_parquet_path)
        df = pd.read_parquet(localpath)

        return df

    @_doc_params(doc_curate=doc_curate)
    def curate(  # type: ignore
        self,
        df: pd.DataFrame,
        column: str = None,
        reference_id: str = "name",
    ) -> pd.DataFrame:
        """Curate index of passed DataFrame to conform with default identifier.

        Args:
            {doc_curate}

        Returns:
            The input DataFrame with the curated index and a boolean `__curated__`
        column that indicates compliance with the default identifier.

        In addition to the .curate() in base class, this also performs alias mapping.
        """
        agg_col = ALIAS_DICT.get(reference_id)
        df = df.copy()

        # if the query column name does not match any columns in the self.df()
        # Bionty assume the query column and the self._id_field uses the same type of
        # identifier
        orig_column = column
        if column is not None and column not in self.df().columns:
            # normalize the identifier column
            if column in df.columns:
                raise ValueError("{column_norm} column already exist!")
            else:
                column = reference_id if column is None else column
                df.rename(columns={orig_column: column}, inplace=True)
            agg_col = ALIAS_DICT.get(column)

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
