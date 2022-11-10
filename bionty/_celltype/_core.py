from functools import cached_property
from typing import Optional

import pandas as pd

from .._ontology import Ontology
from .._table import EntityTable


class CellType(EntityTable):
    """Cell type.

    Edits of terms are coordinated and reviewed on:
    https://github.com/obophenotype/cell-ontology
    """

    def __init__(
        self, id=None, url: Optional[str] = None, reload: bool = False
    ) -> None:
        super().__init__(id=id)
        self._url = url
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
        ).set_index(self._id_field)

    @cached_property
    def ontology(self) -> Ontology:  # type:ignore
        """Cell ontology."""
        if self._url is None:
            self._url = "http://purl.obolibrary.org/obo/cl/cl-simple.obo"

        return super().ontology(url=self._url, reload=self._reload)
