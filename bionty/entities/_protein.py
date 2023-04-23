from functools import cached_property
from typing import Literal, Optional

import pandas as pd

from .._entity import Entity
from .._normalize import NormalizeColumns
from .._settings import s3_bionty_assets
from ._shared_docstrings import _doc_params, doc_entites


@_doc_params(doc_entities=doc_entites)
class Protein(Entity):
    """Protein.

    1. Uniprot
    Edits of terms are coordinated and reviewed on:
    https://www.uniprot.org/

    Args:
        {doc_entities}
    """

    def __init__(
        self,
        species: str = "human",
        database: Optional[Literal["uniprot"]] = None,
        version: Optional[str] = None,
    ) -> None:
        super().__init__(
            database=database,
            version=version,
            species=species,
            reference_id="uniprotkb_id",
        )

    @cached_property
    def df(self) -> pd.DataFrame:
        """DataFrame.

        See ingestion: https://lamin.ai/docs/bionty-assets/ingest/uniprot-protein
        """
        cloudpath = s3_bionty_assets(self._cloud_parquet_path)
        self._filepath = cloudpath.fspath

        df = pd.read_parquet(self._filepath)
        NormalizeColumns.protein(df)
        _get_shortest_name(
            df, "synonyms"
        )  # Take the shortest name in protein names list as name
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
