from typing import Literal, Optional

from .._entity import Entity
from ._shared_docstrings import _doc_params, doc_entites


@_doc_params(doc_entities=doc_entites)
class Tissue(Entity):
    """Tissue.

    1. Uberon
    Edits of terms are coordinated and reviewed on:
    https://github.com/obophenotype/uberon

    Args:
        {doc_entities}
    """

    def __init__(
        self,
        species: str = "all",
        database: Optional[Literal["uberon"]] = None,
        version: Optional[str] = None,
    ) -> None:
        super().__init__(
            database=database, version=version, species=species, prefix="UBERON"
        )
