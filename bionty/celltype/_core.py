from functools import cached_property
from urllib.request import urlretrieve

from .._io import loads_pickle, read_json
from .._models import create_model
from .._settings import check_dynamicdir_exists, settings

CellTypeData = create_model("CellTypeData", __module__=__name__)


class CellType:
    """Cell type bioentity.

    Edits of terms are coordinated and reviewed on:
    https://github.com/obophenotype/cell-ontology
    """

    def __init__(self, reload: bool = False) -> None:
        self._dataclasspath = settings.dynamicdir / "celltypedataclass.pkl"
        filename, _ = urlretrieve(
            "https://bionty-assets.s3.amazonaws.com/cl-simple.json"
        )
        self._onto_dict = read_json(filename)

    @property
    def dataclasspath(self):
        """Path to the picked dataclass."""
        return self._dataclasspath

    @cached_property
    def dataclass(self):
        """Pydantic dataclass of cell types."""
        return self._load_dataclass()

    @cached_property
    def onto_dict(self) -> dict:
        """Keyed by name, valued by label."""
        return self._onto_dict

    @check_dynamicdir_exists
    def _load_dataclass(self):
        """Loading dataclass from the pickle file."""
        if not self.dataclasspath.exists():
            import pickle

            from .._io import write_pickle

            CellTypeData.add_fields(**self.onto_dict)
            write_pickle(pickle.dumps(CellTypeData()), self.dataclasspath)

        return loads_pickle(self.dataclasspath)
