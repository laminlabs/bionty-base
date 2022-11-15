from functools import cached_property
from typing import Optional

import pandas as pd

from .._ontology import Ontology
from .._settings import settings
from .._table import EntityTable


class Tissue(EntityTable):
    """Tissue.

    Edits of terms are coordinated and reviewed on:
    https://github.com/obophenotype/uberon
    """

    def __init__(
        self, id: str = "ontology_id", url: Optional[str] = None, reload: bool = False
    ) -> None:
        super().__init__(id=id)
        self._url = url
        self._reload = reload

    @cached_property
    def df(self) -> pd.DataFrame:
        """DataFrame."""
        self._filepath = settings.datasetdir / "tissue_lookup.parquet"

        if not self._filepath.exists():
            df = self._ontology_to_df(self.ontology)
            df.to_parquet(self._filepath)

        return pd.read_parquet(self._filepath)

    @cached_property
    def ontology(self) -> Ontology:  # type:ignore
        """Uberon multi-species anatomy ontology."""
        if self._url is None:
            self._url = "http://purl.obolibrary.org/obo/uberon/basic.obo"

        return super().ontology(
            url=self._url, reload=self._reload, filename="uberon-basic.obo"
        )
