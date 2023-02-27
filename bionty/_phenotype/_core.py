from typing import Optional

from cached_property import cached_property

from .._entity import Entity
from .._ontology import Ontology

FILENAMES = {
    "human_hp": "phenotype_lookup.parquet",
}


class Phenotype(Entity):
    """Phenotype.

    Args:
        species: `name` of `Species` entity Entity.

    Edits of terms are coordinated and reviewed on:
    https://hpo.jax.org/app/
    """

    def __init__(
        self,
        species: str = "human",
        id: str = "ontology_id",
        database: Optional[str] = None,
        version: Optional[str] = None,
    ) -> None:
        super().__init__(
            id=id,
            database=database,
            version=version,
            species=species,
            filenames=FILENAMES,
        )

    @cached_property
    def ontology(self) -> Ontology:  # type:ignore
        """HPO ontology."""
        return super().ontology()
