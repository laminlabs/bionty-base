from typing import Literal, Optional

import pandas as pd
from cached_property import cached_property

from .._entity import Entity
from .._settings import s3_bionty_assets


class CellMarker(Entity):
    """Cell markers.

    1. Cell Marker Ontology
    Edits of terms are coordinated and reviewed on:
    http://bio-bigdata.hrbmu.edu.cn/CellMarker/

    Args:
        species: `name` of `Species` entity Entity.
    """

    def __init__(
        self,
        species: str = "human",
        database: Optional[Literal["cellmarker"]] = None,
        version: Optional[str] = None,
    ) -> None:
        super().__init__(
            database=database, version=version, species=species, reference_id="name"
        )

    @cached_property
    def df(self):
        """DataFrame.

        See ingestion: https://lamin.ai/docs/bionty-assets/ingest/cell-marker-2.0
        """
        cloudpath = s3_bionty_assets(self._cloud_parquet_path)
        df = pd.read_parquet(cloudpath.fspath)

        return df
