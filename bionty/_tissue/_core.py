from typing import Optional

from .._entity import Entity


class Tissue(Entity):
    """Tissue.

    Edits of terms are coordinated and reviewed on:
    https://github.com/obophenotype/uberon
    """

    def __init__(
        self,
        id: str = "ontology_id",
        database: Optional[str] = None,
        version: Optional[str] = None,
    ) -> None:
        super().__init__(id=id, database=database, version=version)
