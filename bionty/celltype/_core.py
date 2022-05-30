from pronto import Ontology


class Celltype:
    """Cell type bioentity.

    Edits of terms are coordinated and reviewed on:
    https://github.com/obophenotype/cell-ontology
    """

    CL_URL = "http://purl.obolibrary.org/obo/cl/cl-simple.obo"

    def __init__(self) -> None:
        self._cl = Ontology(self.CL_URL)

    @property
    def cl(self):
        """Ontology object of CL."""
        return self._cl
