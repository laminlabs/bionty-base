from typing import Literal, Optional

from .._bionty import Bionty
from ._shared_docstrings import _doc_params, doc_entites


@_doc_params(doc_entities=doc_entites)
class Protein(Bionty):
    """Protein.

    1. Uniprot
    Edits of terms are coordinated and reviewed on:
    https://www.uniprot.org/

    Args:
        {doc_entities}
    """

    def __init__(
        self,
        species: Optional[str] = "human",
        source: Optional[Literal["uniprot"]] = None,
        version: Optional[str] = None,
        **kwargs
    ) -> None:
        super().__init__(source=source, version=version, species=species, **kwargs)
