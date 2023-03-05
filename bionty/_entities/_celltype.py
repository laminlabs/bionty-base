from typing import Optional

from .._entity import Entity


class CellType(Entity):
    """Cell type ontologies.

    1. Cell ontology
    Edits of terms are coordinated and reviewed on:
    https://github.com/obophenotype/cell-ontology

    2. Human cell atlas ontology
    Edits of terms are coordinated and reviewed on:
    https://github.com/HumanCellAtlas/ontology
    """

    def __init__(
        self,
        id: str = "ontology_id",
        species: str = "human",
        database: Optional[str] = None,
        version: Optional[str] = None,
    ) -> None:
        super().__init__(
            id=id,
            database=database,
            version=version,
            species=species,
        )
