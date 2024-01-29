from typing import Literal, Optional

from bionty_base._public_ontology import PublicOntology

from ._shared_docstrings import _doc_params, doc_entites


@_doc_params(doc_entities=doc_entites)
class CellMarker(PublicOntology):
    """Cell markers.

    1. Cell Marker Ontology
    Edits of terms are coordinated and reviewed on:
    http://bio-bigdata.hrbmu.edu.cn/CellMarker/

    Args:
        {doc_entities}
    """

    def __init__(
        self,
        organism: Optional[Literal["human", "mouse"]] = None,
        source: Optional[Literal["cellmarker"]] = None,
        version: Optional[str] = None,
        **kwargs,
    ) -> None:
        super().__init__(source=source, version=version, organism=organism, **kwargs)
