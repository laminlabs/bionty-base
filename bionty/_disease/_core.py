from typing import Optional

import pandas as pd
from cached_property import cached_property

from .._ontology import Ontology
from .._settings import settings
from .._table import EntityTable

FILENAMES = {
    "human_mondo": "human_mondo_lookup.parquet",
    "human_hd": "human_hd_lookup.parquet",
}


class Disease(EntityTable):
    """Disease ontologies.

    1. Mondo
    Edits of terms are coordinated and reviewed on:
    https://github.com/monarch-initiative/mondo

    2. Human Disease Ontology
    Edits of terms are coordinated and reviewed on:
    https://github.com/DiseaseOntology/HumanDiseaseOntology
    """

    def __init__(
        self,
        id: str = "ontology_id",
        species: str = "human",
        database: str = "mondo",
        version: Optional[str] = None,
    ) -> None:
        super().__init__(id=id, database=database, version=version)
        if FILENAMES.get(f"{species}_{database}") is None:
            raise NotImplementedError
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
        """Disease ontology."""
        return super().ontology()
