from typing import Literal, Optional

import pandas as pd

from .._bionty import Bionty
from ..dev._io import s3_bionty_assets
from ._shared_docstrings import _doc_params, doc_entites


@_doc_params(doc_entities=doc_entites)
class CellMarker(Bionty):
    """Cell markers.

    1. Cell Marker Ontology
    Edits of terms are coordinated and reviewed on:
    http://bio-bigdata.hrbmu.edu.cn/CellMarker/

    Args:
        {doc_entities}
    """

    def __init__(
        self,
        species: Optional[str] = "human",
        source: Optional[Literal["cellmarker"]] = None,
        version: Optional[str] = None,
        **kwargs
    ) -> None:
        super().__init__(source=source, version=version, species=species, **kwargs)

    def df(self) -> pd.DataFrame:
        """DataFrame.

        See ingestion: https://lamin.ai/docs/bionty-assets/ingest/cell-marker-2.0
        """
        localpath = s3_bionty_assets(self._parquet_filename)
        df = pd.read_parquet(localpath)

        return df
