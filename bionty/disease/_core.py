from functools import cached_property

from .._ontology import Ontology
from .._settings import dump_dataclass_as_private_module, settings
from .._urls import OBO_MONDO_OWL


class Disease(Ontology):
    """Disease bioentity.

    Edits of terms are coordinated and reviewed on:
    https://github.com/monarch-initiative/mondo
    """

    def __init__(self) -> None:
        self._filepath = settings.dynamicdir / "diseasedata.py"
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
        if not self.filepath.exists():
            from .._models import create_model

            DiseaseData = create_model("DiseaseData", **self.onto_dict)
            dump_dataclass_as_private_module(DiseaseData)

        from .._dynamic.diseasedata import DiseaseData

        return DiseaseData
