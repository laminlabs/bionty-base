from functools import cached_property
from pathlib import Path

import pandas as pd

from .._io import loads_pickle
from .._models import BaseModel, create_model
from .._settings import check_dynamicdir_exists, settings

HERE = Path(__file__).parent
SPECIES_FILENAME = HERE / "tables/Species.csv"


SpeciesData = create_model("SpeciesData", __module__=__name__)


class Entry(BaseModel):
    display_name: str
    scientific_name: str
    common_name: str
    taxon_id: int
    assembly: str
    accession: str
    release: int
    short_name: str


class Species:
    """Species class."""

    def __init__(self, common_name="human") -> None:
        self._std_name = common_name
        self._dataclasspath = settings.dynamicdir / "speciesdata.pkl"

    @cached_property
    def df(self):
        self._df = pd.read_csv(SPECIES_FILENAME, header=0, index_col=0)
        return self._df

    @property
    def std_id(self):
        """common_name is the standardized id for species."""
        return "display_name"

    @property
    def std_name(self):
        """Value of the .std_id."""
        return self._std_name

    @property
    def fields(self):
        return self.df.columns.tolist()

    @property
    def dataclasspath(self):
        """Path to the picked dataclass."""
        return self._dataclasspath

    @cached_property
    def dataclass(self):
        return self._load_dataclass()

    def search(self, field: str):
        """Search species fields based on .std_id.

        Args:
            field: one of .fields
        Returns:
            value of a field

        e.g.
        'common_name': 'human'
        'scientific_name': 'homo_sapiens'
        'short_name': 'hsapiens'
        'taxon_id': 9606
        'assembly': 'GRCh38.p13'

        """
        return self.df[[field]].to_dict()[field][self.std_name]

    @check_dynamicdir_exists
    def _load_dataclass(self):
        """Pydantic data class of genes."""
        if not self.dataclasspath.exists():
            import pickle

            from .._io import write_pickle

            model = self._create_data_model()
            write_pickle(pickle.dumps(model()), self.dataclasspath)

        return loads_pickle(self.dataclasspath)

    def _create_data_model(self):
        """Create the species data model with pydantic."""
        df = self.df.reset_index()
        for i in df.index:
            entry = {}
            entry.update({col: df.loc[i][col] for col in df.columns})
            SpeciesData.add_fields(**{df.loc[i][self.std_id]: (Entry, Entry(**entry))})

        return SpeciesData
