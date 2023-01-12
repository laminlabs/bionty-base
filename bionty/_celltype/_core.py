from typing import Optional

import pandas as pd
from cached_property import cached_property

from .._ontology import Ontology
from .._settings import settings
from .._table import EntityTable


class CellType(EntityTable):
    """Cell type.

    Edits of terms are coordinated and reviewed on:
    https://github.com/obophenotype/cell-ontology
    """

    def __init__(
        self,
        id: str = "ontology_id",
        database: Optional[str] = None,
        version: Optional[str] = None,
    ) -> None:
        database = "cl" if database is None else database
        super().__init__(id=id, database=database, version=version)

    @cached_property
    def df(self) -> pd.DataFrame:
        """DataFrame."""
        self._filepath = settings.datasetdir / "celltype_lookup.parquet"

        if not self._filepath.exists():
            df = self._ontology_to_df(self.ontology)
            df.to_parquet(self._filepath)

        return pd.read_parquet(self._filepath).reset_index().set_index(self._id_field)

    @cached_property
    def ontology(self) -> Ontology:  # type:ignore
        """Cell ontology."""
        return super().ontology()
