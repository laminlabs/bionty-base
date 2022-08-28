from functools import cached_property

import pandas as pd

from .._ontology import Ontology
from .._settings import settings
from .._table import EntityTable


class Tissue(EntityTable):
    """Tissue.

    Edits of terms are coordinated and reviewed on:
    https://github.com/obophenotype/uberon
    """

    def __init__(self, reload=False) -> None:
        super().__init__(id=id)
        self._reload = reload
        self._filepath = settings.dynamicdir / "uberon-basic.obo"

    @cached_property
    def df(self) -> pd.DataFrame:
        """DataFrame."""
        return pd.DataFrame(
            [
                (term.id, term.name)
                for term in self.ontology.terms()
                if term.id.startswith("UBERON:")
            ],
            columns=["id", "name"],
        ).set_index("id")

    @cached_property
    def ontology(self):
        """Uberon multi-species anatomy ontology."""
        url = "http://purl.obolibrary.org/obo/uberon/basic.obo"
        url = url if ((not self._filepath.exists()) or (self._reload)) else None
        ontology_ = Ontology(handle=self._filepath, url=url)
        if url is not None:
            ontology_.write_obo(filename="uberon-basic.obo")
        return ontology_
