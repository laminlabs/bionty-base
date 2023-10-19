from typing import Literal, Optional

from .._bionty import Bionty
from ._shared_docstrings import _doc_params, doc_entites


@_doc_params(doc_entities=doc_entites)
class Ethnicity(Bionty):
    """Ethnicity.

    1. Human Ancestry Ontology
    Edits of terms are coordinated and reviewed on:
    https://github.com/EBISPOT/hancestro

    Args:
        {doc_entities}
    """

    def __init__(
        self,
        organism: Optional[str] = None,
        source: Optional[Literal["hancestro"]] = None,
        version: Optional[str] = None,
        **kwargs
    ) -> None:
        super().__init__(
            source=source,
            version=version,
            organism=organism,
            include_id_prefixes={"hancestro": ["HANCESTRO"]},
            **kwargs
        )
