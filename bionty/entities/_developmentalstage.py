from typing import Literal, Optional

from .._bionty import Bionty
from ._shared_docstrings import _doc_params, doc_entites


@_doc_params(doc_entities=doc_entites)
class DevelopmentalStage(Bionty):
    """Developmental Stage.

    1. Developmental Stage Ontology
    Edits of terms are coordinated and reviewed on:
    https://github.com/obophenotype/developmental-stage-ontologies

    Args:
        {doc_entities}
    """

    def __init__(
        self,
        species: Optional[str] = None,
        source: Optional[Literal["hsapdv", "mmusdv"]] = None,
        version: Optional[str] = None,
        **kwargs
    ) -> None:
        super().__init__(
            source=source,
            version=version,
            species=species,
            include_id_prefixes={"hsapdv": ["HsapDv"], "mmusdv": ["MmusDv"]},
            **kwargs
        )
