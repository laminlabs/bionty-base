import json
from typing import Literal, Optional

import pandas as pd

from .._entity import Bionty
from ..dev._io import s3_bionty_assets
from ._shared_docstrings import _doc_params, doc_entites


@_doc_params(doc_entities=doc_entites)
class BFXPipeline(Bionty):
    """Bioinformatics pipelines.

    Args:
        {doc_entities}
    """

    def __init__(
        self,
        species: str = "all",
        source: Optional[Literal["lamin"]] = None,
        version: Optional[str] = None,
        **kwargs
    ) -> None:
        super().__init__(
            source=source, version=version, species=species, reference_id="id", **kwargs
        )

    def df(self) -> pd.DataFrame:
        """DataFrame."""
        localpath = s3_bionty_assets(filename="bfxpipelines.json")
        with open(localpath, "r") as f:
            data = json.load(f)

        df = pd.DataFrame(data).transpose()

        return df
