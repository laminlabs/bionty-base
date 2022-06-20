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

    def __init__(self) -> None:
        self._filepath = settings.datasetdir / "disease.pickle"
        if not self.filepath.exists():
            super().__init__(base_iri=OBO_MONDO_OWL, load=True)

    @property
    def filepath(self):
        return self._filepath

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
        model.add_fields(**self._load_model_dict())
        return model(**{"name": "disease", "std_id": "mondo_id"})

    @check_datasetdir_exists
    def _load_model_dict(self):
        """Load pickle file."""
        if not self.filepath.exists():
            from .._io import write_pickle

            write_pickle(self.onto_dict, self.filepath)

        return read_pickle(self.filepath)
