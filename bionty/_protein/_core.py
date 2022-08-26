from functools import cached_property

import pandas as pd

from .._normalize import NormalizeColumns
from .._settings import check_datasetdir_exists, settings


def _get_shortest_name(df, column):
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

    df[column.rstrip("s")] = name_list
    df[column] = names_list


class Protein:
    """Protein.

    Args:
        species: `common_name` of `Species` entity EntityTable.
    """

    def __init__(self, species="human", id=None) -> None:
        self._species = species
        self._filepath = settings.datasetdir / f"uniprot-{self.species}.feather"
        self._id_field = "uniprotkb_id" if id is None else id

    @property
    def entity(self):
        """Name of the entity."""
        return "protein"

    @property
    def species(self):
        """The `common_name` of `Species` entity EntityTable."""
        return self._species

    @property
    def filepath(self):
        """The local filepath to the DataFrame."""
        return self._filepath

    @cached_property
    def df(self):
        """DataFrame."""
        if self.species not in {"human", "mouse"}:
            raise NotImplementedError
        else:
            if not self.filepath.exists():
                self._download_df()
            df = pd.read_feather(self.filepath)
            NormalizeColumns.protein(df)
            _get_shortest_name(df, "protein_names")
            return df.set_index(self._id_field)

    @check_datasetdir_exists
    def _download_df(self):
        from urllib.request import urlretrieve

        urlretrieve(
            f"https://bionty-assets.s3.amazonaws.com/uniprot-{self.species}.feather",
            self.filepath,
        )
