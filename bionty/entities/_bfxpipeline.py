import json
from pathlib import Path
from typing import Literal, Optional

import pandas as pd

from .._bionty import Bionty
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
        organism: Optional[Literal["all"]] = None,
        source: Optional[Literal["lamin"]] = None,
        version: Optional[str] = None,
        **kwargs
    ) -> None:
        super().__init__(source=source, version=version, organism=organism, **kwargs)

    def _load_df(self) -> pd.DataFrame:
        localpath = self._local_parquet_path.as_posix().replace(  # type:ignore
            ".parquet", ".json"
        )
        s3_bionty_assets("bfxpipelines.json", Path(localpath))
        with open(localpath, "r") as f:
            data = json.load(f)

        df = pd.DataFrame(data).transpose()

        return df.reset_index()

    def df(self) -> pd.DataFrame:
        """Pandas DataFrame of the ontology.

        Returns:
            A Pandas DataFrame of the ontology.

        Examples:
            >>> import bionty as bt
            >>> bt.BFXPipeline().df()
        """
        return self._df.set_index("id")
