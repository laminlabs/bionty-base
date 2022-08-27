from functools import cached_property

import pandas as pd

from .._ontology import Ontology
from .._settings import settings
from .._table import EntityTable


class CellType(EntityTable):
    """Cell type.

    Edits of terms are coordinated and reviewed on:
    https://github.com/obophenotype/cell-ontology
    """

    def __init__(self, reload=False) -> None:
        self._reload = reload

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
        ).set_index("id")

    @cached_property
    def ontology(self):
        """Cell ontology."""
        url = "http://purl.obolibrary.org/obo/cl/cl-simple.obo"
        localpath = settings.dynamicdir / "cl-simple.obo"
        url = url if ((not localpath.exists()) or (self._reload)) else None
        ontology_ = Ontology(handle=localpath, url=url)
        if url is not None:
            ontology_.write_obo()
        return ontology_
