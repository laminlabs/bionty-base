from .._ontology import Ontology
from .._urls import OBO_CL_OWL


class CellType(Ontology):
    """Cell type bioentity.

    Edits of terms are coordinated and reviewed on:
    https://github.com/obophenotype/cell-ontology
    """

    def __init__(self, base_iri=OBO_CL_OWL, load: bool = True) -> None:
        super().__init__(base_iri=base_iri, load=load)
