from functools import cached_property

from .._io import read_pickle
from .._models import create_model
from .._ontology import Ontology
from .._settings import check_datasetdir_exists, settings
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
        model.add_fields(**self.load_model_dict())
        return model(**{"name": "disease", "std_id": "mondo_id"})

    @check_datasetdir_exists
    def load_model_dict(self):
        """Pydantic data class of diseases."""
        filepath = settings.datasetdir / "disease.pickle"

        if not filepath.exists():
            from .._io import write_pickle

            write_pickle(self.onto_dict, filepath)

        return read_pickle(filepath)
