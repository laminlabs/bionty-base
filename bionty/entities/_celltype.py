from typing import Literal, Optional

from .._entity import Bionty
from ._shared_docstrings import _doc_params, doc_entites


@_doc_params(doc_entities=doc_entites)
class CellType(Bionty):
    """Cell type ontologies.

    1. Cell ontology
    Edits of terms are coordinated and reviewed on:
    https://github.com/obophenotype/cell-ontology

    2. Human cell atlas ontology
    Edits of terms are coordinated and reviewed on:
    https://github.com/HumanCellAtlas/ontology

    Args:
        {doc_entities}
    """

    def __init__(
        self,
        species: str = "human",
        source: Optional[Literal["cl", "ca"]] = None,
        version: Optional[str] = None,
        **kwargs
    ) -> None:
        super().__init__(
            source=source,
            version=version,
            species=species,
            include_id_prefixes={"cl": ["CL"]},
            **kwargs
        )
