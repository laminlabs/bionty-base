from typing import Literal, Optional

from .._entity import Entity
from ._shared_docstrings import _doc_params, doc_entites


@_doc_params(doc_entities=doc_entites)
class BFXPipelines(Entity):
    """Bioinformatics pipelines.

    Args:
        {doc_entities}
    """

    def __init__(
        self,
        species: str = "human",
        database: Optional[Literal["lamin"]] = None,
        version: Optional[str] = None,
    ) -> None:
        super().__init__(
            database=database,
            version=version,
            species=species,
        )
