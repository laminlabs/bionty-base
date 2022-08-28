from functools import cached_property

import pandas as pd

from .._settings import settings
from .._table import EntityTable


class CellType(EntityTable):
    """Cell type.

    Edits of terms are coordinated and reviewed on:
    https://github.com/obophenotype/cell-ontology
    """

    def __init__(self, id=None, reload=False) -> None:
        self._reload = reload
        super().__init__(id=id)
        self._filepath = settings.dynamicdir / "cl-simple.obo"

    @cached_property
    def df(self) -> pd.DataFrame:
        """DataFrame."""
        return pd.DataFrame(
            [
                (term.id, term.name)
                for term in self.ontology.terms()
                if term.id.startswith("CL:")
            ],
            columns=["id", "name"],
        ).set_index(self._id_field)

    @cached_property
    def ontology(self):
        """Cell ontology."""
        url = "http://purl.obolibrary.org/obo/cl/cl-simple.obo"
        url = url if ((not self._filepath.exists()) or (self._reload)) else None
        ontology_ = self._Ontology(handle=self._filepath, url=url)
        if url is not None:
            ontology_.write_obo()
        return ontology_
