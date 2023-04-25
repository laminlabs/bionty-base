import json
from functools import cached_property
from typing import Literal, Optional

import pandas as pd

from .._entity import Entity
from .._settings import s3_bionty_assets
from ._shared_docstrings import _doc_params, doc_entites


@_doc_params(doc_entities=doc_entites)
class BFXPipelines(Entity):
    """Bioinformatics pipelines.

    Args:
        {doc_entities}
    """

    def __init__(
        self,
        species: str = "human",
        database: Optional[Literal["lamin"]] = None,
        version: Optional[str] = None,
    ) -> None:
        super().__init__(
            database=database,
            version=version,
            species=species,
        )

    @cached_property
    def df(self):
        """DataFrame."""
        localpath = s3_bionty_assets(filename="bfxpipelines.json")
        with open(localpath, "r") as f:
            data = json.load(f)

        df = pd.DataFrame(data)

        return df
