from typing import Literal, Optional

from .._entity import Bionty
from ._shared_docstrings import _doc_params, doc_entites


@_doc_params(doc_entities=doc_entites)
class Disease(Bionty):
    """Disease ontologies.

    1. Mondo
    Edits of terms are coordinated and reviewed on:
    https://github.com/monarch-initiative/mondo

    2. Human Disease Ontology
    Edits of terms are coordinated and reviewed on:
    https://github.com/DiseaseOntology/HumanDiseaseOntology

    Args:
        {doc_entities}
    """

    def __init__(
        self,
        species: Optional[str] = None,
        source: Optional[Literal["mondo", "doid"]] = None,
        version: Optional[str] = None,
        **kwargs
    ) -> None:
        super().__init__(
            source=source,
            version=version,
            species=species,
            include_id_prefixes={"mondo": ["MONDO"]},
            **kwargs
        )
