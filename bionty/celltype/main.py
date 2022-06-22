from functools import cached_property

from .._io import loads_pickle
from .._models import create_model
from .._ontology import Ontology
from .._settings import check_dynamicdir_exists, settings
from .._urls import OBO_CL_OWL

CellTypeData = create_model("CellTypeData", __module__=__name__)


class CellType(Ontology):
    """Cell type bioentity.

    Edits of terms are coordinated and reviewed on:
    https://github.com/obophenotype/cell-ontology
    """

    def __init__(self) -> None:
        self._dataclasspath = settings.dynamicdir / "celltypedataclass.pkl"
        if not self.dataclasspath.exists():
            super().__init__(base_iri=OBO_CL_OWL, load=True)

    @property
    def dataclasspath(self):
        """Path to the picked dataclass."""
        return self._dataclasspath

    @cached_property
    def onto_dict(self) -> dict:
        """Keyed by name, valued by label."""
        return {
            v.name: v.label[0]
            for k, v in self.classes.items()
            if k.startswith("CL") & len(v.label) > 0
        }

    @cached_property
    def dataclass(self):
        """Pydantic dataclass of cell types."""
        return self._load_dataclass()

    @check_dynamicdir_exists
    def _load_dataclass(self):
        """Loading dataclass from the pickle file."""
        if not self.dataclasspath.exists():
            import pickle

            from .._io import write_pickle

            CellTypeData.add_fields(**self.onto_dict)
            write_pickle(pickle.dumps(CellTypeData()), self.dataclasspath)

        return loads_pickle(self.dataclasspath)
