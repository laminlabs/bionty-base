from collections import namedtuple
from functools import cached_property

import pandas as pd

from .._normalize import NormalizeColumns
from .._settings import check_datasetdir_exists, settings
from .._table import EntityTable, _todict


def _get_shortest_name(df, column, new_column="name"):
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


class Protein(EntityTable):
    """Protein.

    Args:
        species: `common_name` of `Species` entity EntityTable.
    """

    def __init__(self, species="human", id=None) -> None:
        super().__init__(id=id)
        if species not in {"human", "mouse"}:
            raise NotImplementedError
        self._species = species
        self._filepath = settings.datasetdir / f"uniprot-{self.species}.feather"
        self._id_field = "uniprotkb_id" if id is None else id

    @property
    def species(self):
        """The `common_name` of `Species` entity EntityTable."""
        return self._species

    @cached_property
    def df(self):
        """DataFrame.

        See ingestion: https://lamin.ai/docs/bionty-assets/ingest/2022-08-26-uniprot
        """
        if not self._filepath.exists():
            self._download_df()
        df = pd.read_feather(self._filepath)
        NormalizeColumns.protein(df)
        _get_shortest_name(
            df, "synonyms"
        )  # Take the shortest name in protein names list as name
        return df.set_index(self._id_field)

    @cached_property
    def lookup(self):
        """Lookup object for auto-complete."""
        values = _todict(self.df.index.values)
        nt = namedtuple(self._id_field, values.keys())

        return nt(**values)

    @check_datasetdir_exists
    def _download_df(self):
        from urllib.request import urlretrieve

        urlretrieve(
            f"https://bionty-assets.s3.amazonaws.com/uniprot-{self.species}.feather",
            self._filepath,
        )
