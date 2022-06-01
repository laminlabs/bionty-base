from .._ontology import Ontology
from .._urls import OBO_MONDO_OWL


class Disease(Ontology):
    """Disease bioentity.

    Edits of terms are coordinated and reviewed on:
    https://github.com/monarch-initiative/mondo
    """

    def __init__(self, base_iri=OBO_MONDO_OWL, load: bool = True) -> None:
        super().__init__(base_iri=base_iri, load=load)
