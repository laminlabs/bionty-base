from functools import cached_property
from urllib.request import urlretrieve

import pandas as pd

from .._io import read_json
from .._table import EntityTable


class CellType(EntityTable):
    """Cell type.

    Edits of terms are coordinated and reviewed on:
    https://github.com/obophenotype/cell-ontology
    """

    def __init__(self) -> None:
        filename, _ = urlretrieve(
            "https://bionty-assets.s3.amazonaws.com/cl-simple.json"
        )
        self._onto_dict = read_json(filename)

    @cached_property
    def df(self) -> pd.DataFrame:
        """DataFrame."""
        return pd.DataFrame(pd.Series(self._onto_dict))
