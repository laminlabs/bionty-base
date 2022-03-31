import pandas as pd
import logging as logg


class Species:

    """Species related bio entities"""

    def __init__(self):
        self._df = pd.read_csv("tables/Species.csv", header=0, index_col=0)

    @property
    def common_name(self):
        """Common names list"""
        return self._df.index.tolist()

    @classmethod
    def attributes(cls):
        return [
            "common_name",
            "scientific_name",
            "short_name",
            "taxon_id",
            "ensembl_assembly",
        ]

    @classmethod
    def get_attribute(cls, attr: str):
        """Get attribute values based on common_name

        parameters
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

        """
        return cls._df[[attr]].to_dict()[attr]


def _format_ensembl_download():
    """Ensembl annotated species and their most recent assemblies

    From: https://useast.ensembl.org/info/about/species.html
    """
    df = pd.read_csv("tables/Species.csv", header=0, index_col=0)
    df.index.name = "common_name"
    df.index = df.index.str.lower()
    df["short_name"] = [
        f'{i[0].lower()}{i.split(" ")[-1]}' for i in df["Scientific name"]
    ]
    df.columns = [i.lower().relace(" ", "_") for i in df.columns]
    df.to_csv("tables/Species.csv", header=True, index=True)
    logg.info("Formated Species.csv!")
