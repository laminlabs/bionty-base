from pathlib import Path
import pandas as pd
import logging as logg


HERE = Path(__file__).parent
SPECIES_FILENAME = HERE / "tables/Species.csv"


class Species:

    """Species related bio entities"""

    _df = pd.read_csv(SPECIES_FILENAME, header=0, index_col=0)

    def __init__(self, species="human"):
        self._common_name = species

    @property
    def common_name(self):
        """Common names list"""
        return self._common_name

    @property
    def attributes(self):
        return [
            "common_name",
            "scientific_name",
            "short_name",
            "taxon_id",
            "ensembl_assembly",
        ]

    def get_attribute(self, attr: str):
        """Get attribute values based on common_name

        Parameters
        ----------
        attr
            one of ['common_name', 'scientific_name', 'short_name', 'taxon_id',
            'ensembl_assembly']

        e.g.
        'common_name': 'human'
        'scientific_name': 'Homo sapiens'
        'short_name': 'hsapiens'
        'taxon_id': 9606
        'ensembl_assembly': 'GRCh38.p13'


        Returns
        -------
        a dict of {'common_name': attr}
        """
        return self._df[[attr]].to_dict()[attr][self.common_name]


def _format_ensembl_download():
    """Ensembl annotated species and their most recent assemblies

    From: https://useast.ensembl.org/info/about/species.html
    """
    df = pd.read_csv(SPECIES_FILENAME, header=0, index_col=0)
    df.index.name = "common_name"
    df.columns = [i.lower().replace(" ", "_") for i in df.columns]
    df.index = df.index.str.lower()
    df["short_name"] = [
        f'{i[0].lower()}{i.split(" ")[-1]}' for i in df["scientific_name"]
    ]
    df.to_csv(SPECIES_FILENAME, header=True, index=True)
    logg.info("Formated Species.csv!")
