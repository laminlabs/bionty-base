from typing import Optional

import pandas as pd
from cached_property import cached_property

from .._ontology import Ontology
from .._settings import settings
from .._table import EntityTable

FILENAMES = {
    "human_hp": "phenotype_lookup.parquet",
    "all_phenio": "phenio_lookup.parquet",
}


class Phenotype(EntityTable):
    """Phenotype ontology.

    1. Human phenotype ontology
    Edits of terms are coordinated and reviewed on:
    https://hpo.jax.org/app/

    2. Phenomics Integrated Ontology (PHENIO)
    Edits of terms are coordinated and reviewed on:
    https://github.com/monarch-initiative/phenio
    Set species to "all" to use it.
    """

    def __init__(
        self,
        species: str = "human",
        id: str = "ontology_id",
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
        """HPO ontology."""
        return super().ontology()
