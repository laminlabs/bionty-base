from typing import Literal, Optional

from .._entity import Entity
from ._shared_docstrings import _doc_params, doc_entites


@_doc_params(doc_entities=doc_entites)
class Phenotype(Entity):
    """Phenotype.

    1. Human Phenotype Ontology
    Edits of terms are coordinated and reviewed on:
    https://hpo.jax.org/app/

    Args:
        {doc_entities}
    """

    def __init__(
        self,
        species: str = "human",
        source: Optional[Literal["hp"]] = None,
        version: Optional[str] = None,
        **kwargs
    ) -> None:
        super().__init__(source=source, version=version, species=species, **kwargs)
