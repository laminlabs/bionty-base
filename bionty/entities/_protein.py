from typing import Literal, Optional

import pandas as pd

from .._entity import Bionty
from .._normalize import NormalizeColumns
from ..dev._io import s3_bionty_assets
from ._shared_docstrings import _doc_params, doc_entites


@_doc_params(doc_entities=doc_entites)
class Protein(Bionty):
    """Protein.

    1. Uniprot
    Edits of terms are coordinated and reviewed on:
    https://www.uniprot.org/

    Args:
        {doc_entities}
    """

    def __init__(
        self,
        species: Optional[str] = "human",
        source: Optional[Literal["uniprot"]] = None,
        version: Optional[str] = None,
        **kwargs
    ) -> None:
        super().__init__(
            source=source,
            version=version,
            species=species,
            reference_id="uniprotkb_id",
            **kwargs
        )

    def df(self) -> pd.DataFrame:
        """DataFrame.

        See ingestion: https://lamin.ai/docs/bionty-assets/ingest/uniprot-protein
        """
        self._filepath = s3_bionty_assets(self._parquet_filename)

        df = pd.read_parquet(self._filepath)
        NormalizeColumns.protein(df)
        _get_shortest_name(
            df, "synonyms"
        )  # Take the shortest name in protein names list as name
        try:
            # for pandas > 2.0
            if not pd.api.types.is_any_real_numeric_dtype(df.index):
                df = df.reset_index().copy()
        except AttributeError:
            if not df.index.is_numeric():
                df = df.reset_index().copy()
        df = df[~df[self.reference_id].isnull()]

        return df


def _get_shortest_name(df: pd.DataFrame, column: str, new_column="name"):
    """Get a single shortest name from a column of lists."""
    name_list = []
    names_list = []
    for lst in df[column]:
        lst = lst.replace(", ", "|")
        names_list.append(lst)

        def shortest_name(lst: list):
            return min(lst, key=len)

        names = lst.split("|")
        no_space_names = [i for i in names if " " not in i]
        if len(no_space_names) == 0:
            name = shortest_name(names)
        else:
            name = shortest_name(no_space_names)
        name_list.append(name)

    df[new_column] = name_list
    df[column] = names_list
