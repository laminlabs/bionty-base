from typing import Optional

from .._entity import Entity
from ._shared_docstrings import _doc_params, doc_entites


class Phenotype(Entity):
    """Phenotype.

    Edits of terms are coordinated and reviewed on:
    https://hpo.jax.org/app/
    """

    @_doc_params(doc_entities=doc_entites)
    def __init__(
        self,
        species: str = "human",
        id: str = "ontology_id",
        database: Optional[str] = None,
        version: Optional[str] = None,
    ) -> None:
        """Test.

        Args:
            {doc_entities}
        """
        super().__init__(
            id=id,
            database=database,
            version=version,
            species=species,
        )
