from functools import cached_property

import pandas as pd

from .._settings import settings
from .._table import EntityTable


class Disease(EntityTable):
    """Disease.

    Edits of terms are coordinated and reviewed on:
    https://github.com/monarch-initiative/mondo
    """

    def __init__(self, id=None, reload: bool = False) -> None:
        super().__init__(id=id)
        self._reload = reload
        self._filepath = settings.dynamicdir / "mondo.obo"

    @cached_property
    def df(self) -> pd.DataFrame:
        """DataFrame."""
        return pd.DataFrame(
            [
                (term.id, term.name)
                for term in self.ontology.terms()
                if term.id.startswith("MONDO:")
            ],
            columns=["id", "name"],
        ).set_index("id")

    @cached_property
    def ontology(self):
        """Uberon multi-species anatomy ontology."""
        url = "http://purl.obolibrary.org/obo/mondo.obo"
        url = url if ((not self._filepath.exists()) or (self._reload)) else None
        ontology_ = self._Ontology(handle=self._filepath, url=url)
        if url is not None:
            ontology_.write_obo(filename="mondo.obo")
        return ontology_
