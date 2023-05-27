from typing import Literal, Optional

from .._entity import Bionty
from ._shared_docstrings import _doc_params, doc_entites


@_doc_params(doc_entities=doc_entites)
class Pathway(Bionty):
    """Pathway.

    1. Pathway Ontology
    Edits of terms are coordinated and reviewed on:
    https://bioportal.bioontology.org/ontologies/PW/?p=summary

    Args:
        {doc_entities}
    """

    def __init__(
        self,
        species: str = "human",
        source: Optional[Literal["pw"]] = None,
        version: Optional[str] = "7.74",  # change to None after fixing 7.78
        **kwargs
    ) -> None:
        super().__init__(source=source, version=version, species=species, **kwargs)
