from .._ontology import Ontology
from .._urls import OBO_CL_OWL


class Celltype:
    """Cell type bioentity.

    Edits of terms are coordinated and reviewed on:
    https://github.com/obophenotype/cell-ontology
    """

    def __init__(self) -> None:
        self._cl = Ontology(OBO_CL_OWL)

    @property
    def cl(self):
        """Ontology object of CL."""
        return self._cl
