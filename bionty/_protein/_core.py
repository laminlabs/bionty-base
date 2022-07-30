from functools import cached_property

import pandas as pd

from .._settings import check_datasetdir_exists, settings


class Protein:
    """Protein.

    Args:
        species: `common_name` of `Species` entity EntityTable.
    """

    def __init__(self, species="human") -> None:
        self._species = species
        self._filepath = settings.datasetdir / f"{self.species}-uniprot.feather"

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
            return pd.read_feather(self.filepath).set_index("UniProtKB-AC")

    @check_datasetdir_exists
    def _download_df(self):
        from urllib.request import urlretrieve

        urlretrieve(
            f"https://bionty-assets.s3.amazonaws.com/{self.species}-uniprot.feather",
            self.filepath,
        )
