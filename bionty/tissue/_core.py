from .._ontology import Ontology
from .._urls import OBO_UBERON_OWL


class Tissue(Ontology):
    """Tissue bioentity.

    Edits of terms are coordinated and reviewed on:
    https://github.com/obophenotype/uberon
    """

    def __init__(self, base_iri=OBO_UBERON_OWL, load: bool = True) -> None:
        super().__init__(base_iri=base_iri, load=load)
