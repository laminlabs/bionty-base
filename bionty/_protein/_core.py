from typing import Optional

import pandas as pd
from cached_property import cached_property

from .._entity import Entity
from .._normalize import NormalizeColumns
from .._settings import s3_bionty_assets


def _get_shortest_name(df: pd.DataFrame, column: str, new_column="name"):
    """Get a single shortest name from a column of lists."""
    name_list = []
    names_list = []
    for i in df[column]:
        i = i.replace(", ", "|")
        names_list.append(i)

        def shortest_name(lst: list):
            return min(lst, key=len)

        names = i.split("|")
        no_space_names = [i for i in names if " " not in i]
        if len(no_space_names) == 0:
            name = shortest_name(names)
        else:
            name = shortest_name(no_space_names)
        name_list.append(name)

    df[new_column] = name_list
    df[column] = names_list


class Protein(Entity):
    """Protein.

    Args:
        species: `name` of `Species` Entity.
    """

    def __init__(
        self,
        species: str = "human",
        id: Optional[str] = None,
        database: Optional[str] = None,
        version: Optional[str] = None,
    ) -> None:
        super().__init__(id=id, database=database, version=version, species=species)
        self._id_field = "uniprotkb_id" if id is None else id

    @cached_property
    def df(self):
        """DataFrame.

        See ingestion: https://lamin.ai/docs/bionty-assets/ingest/uniprot-protein
        """
        cloudpath = s3_bionty_assets(self._cloud_file_path)
        self._filepath = cloudpath.fspath

        df = pd.read_parquet(self._filepath)
        NormalizeColumns.protein(df)
        _get_shortest_name(
            df, "synonyms"
        )  # Take the shortest name in protein names list as name
        if not df.index.is_numeric():
            df = df.reset_index().copy()
        df = df[~df[self._id_field].isnull()]
        return df.set_index(self._id_field)
