from typing import Optional

from .._entity import Entity


class CellLine(Entity):
    """Cell line.

    Args:
        species: `name` of `Species` entity Entity.

    Edits of terms are coordinated and reviewed on:
    https://github.com/CLO-ontology/CLO
    """

    def __init__(
        self,
        species: str = "human",
        id: str = "ontology_id",
        database: Optional[str] = None,
        version: Optional[str] = None,
    ) -> None:
        super().__init__(
            id=id,
            database=database,
            version=version,
            species=species,
        )
