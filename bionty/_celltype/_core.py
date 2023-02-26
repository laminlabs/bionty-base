from typing import Optional

import pandas as pd
from cached_property import cached_property

from .._entity import Entity
from .._ontology import Ontology
from .._settings import settings

FILENAMES = {
    "human_cl_ontology": "human_cl_lookup.parquet",
    "human_ca": "human_ca_lookup.parquet",
}


class CellType(Entity):
    """Cell type ontologies.

    1. Cell ontology
    Edits of terms are coordinated and reviewed on:
    https://github.com/obophenotype/cell-ontology

    2. Human cell atlas ontology
    Edits of terms are coordinated and reviewed on:
    https://github.com/HumanCellAtlas/ontology
    """

    def __init__(
        self,
        id: str = "ontology_id",
        species: str = "human",
        database: Optional[str] = None,
        version: Optional[str] = None,
    ) -> None:
        super().__init__(id=id, database=database, version=version)
        self._species = species

    @property
    def species(self):
        """The `name` of `Species` entity EntityTable."""
        return self._species

    @cached_property
    def df(self) -> pd.DataFrame:
        """DataFrame."""
        self._filepath = settings.datasetdir / FILENAMES.get(
            f"{self.species}_{self.database}"
        )

        if not self._filepath.exists():
            df = self._ontology_to_df(self.ontology)
            df.to_parquet(self._filepath)

        return pd.read_parquet(self._filepath).reset_index().set_index(self._id_field)

    @cached_property
    def ontology(self) -> Ontology:  # type:ignore
        """Cell ontology."""
        return super().ontology()
