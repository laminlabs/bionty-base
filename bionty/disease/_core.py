from functools import cached_property

from .._io import loads_pickle, write_pickle
from .._models import create_model
from .._ontology import Ontology
from .._settings import check_dynamicdir_exists, settings
from .._urls import OBO_MONDO_OWL

DiseaseData = create_model("DiseaseData", __module__=__name__)


class Disease(Ontology):
    """Disease bioentity.

    Edits of terms are coordinated and reviewed on:
    https://github.com/monarch-initiative/mondo
    """

    def __init__(self) -> None:
        self._filepath = settings.dynamicdir / "diseasedata.pkl"
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

    @check_dynamicdir_exists
    def dataclass(self):
        """Pydantic data class of diseases."""
        if not self.filepath.exists():
            import pickle

            DiseaseData.add_fields(**Disease().onto_dict)
            write_pickle(pickle.dumps(DiseaseData()), self.filepath)

        return loads_pickle(self.filepath)
