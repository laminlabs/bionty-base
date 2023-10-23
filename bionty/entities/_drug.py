from typing import Literal, Optional

from .._bionty import Bionty
from ._shared_docstrings import _doc_params, doc_entites


@_doc_params(doc_entities=doc_entites)
class Drug(Bionty):
    """Drug ontologies.

    1. DRON
    Edits of terms are coordinated and reviewed on:
    https://bioportal.bioontology.org/ontologies/DRON/

    Args:
        {doc_entities}
    """

    def __init__(
        self,
        organism: Optional[Literal["all"]] = None,
        source: Optional[Literal["dron"]] = None,
        version: Optional[str] = None,
        **kwargs
    ) -> None:
        super().__init__(
            source=source,
            version=version,
            organism=organism,
            include_id_prefixes={"dron": ["DRON"]},
            **kwargs
        )
