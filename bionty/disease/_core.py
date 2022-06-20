from functools import cached_property

from .._models import create_model
from .._ontology import Ontology
from .._urls import OBO_MONDO_OWL


class Disease(Ontology):
    """Disease bioentity.

    Edits of terms are coordinated and reviewed on:
    https://github.com/monarch-initiative/mondo
    """

    def __init__(self, base_iri=OBO_MONDO_OWL, load: bool = True) -> None:
        super().__init__(base_iri=base_iri, load=load)

    @cached_property
    def onto_dict(self) -> dict:
        """Keyed by name, valued by label."""
        return {
            v.name: v.label[0]
            for k, v in self.classes.items()
            if k.startswith("MONDO") & len(v.label) > 0
        }

    @cached_property
    def data_class(self):
        """Pydantic data class of diseases."""
        model = create_model("Disease")
        model.add_fields(**self.onto_dict)
        return model(**{"name": "disease", "std_id": "mondo_id"})
