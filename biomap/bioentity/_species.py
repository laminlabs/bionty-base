import pandas as pd


class Species:

    """Species related bio entities"""

    @classmethod
    def common_name(cls):
        """Common names list"""
        return ensembl().index.tolist()

    @classmethod
    def scientific_name(cls):
        """Common name : Scientific name

        e.g. {'human': 'Homo sapiens'}

        """
        return ensembl()[["Scientific name"]].to_dict()["Scientific name"]

    @classmethod
    def short_name(cls):
        """Common name : Short name

        e.g. {'human': 'hsapiens'}

        """
        return ensembl()[["Short name"]].to_dict()["Short name"]

    @classmethod
    def taxon_id(cls):
        """Common name : Taxon ID

        e.g. {'human': 9606}

        """
        return ensembl()[["Taxon ID"]].to_dict()["Taxon ID"]

    @classmethod
    def ensembl_assembly(cls):
        """Common name : Ensembl Assembly

        e.g. {'human': 'Homo sapiens': 'GRCh38.p13'}

        """
        return ensembl()[["Ensembl Assembly"]].to_dict()["Ensembl Assembly"]


def ensembl():
    """Ensembl annotated species and their most recent assemblies

    From: https://useast.ensembl.org/info/about/species.html
    """
    df = pd.read_csv("tables/Species.csv", header=0, index_col=0)
    df.index = df.index.str.lower()
    df["Short name"] = [
        f'{i[0].lower()}{i.split(" ")[-1]}' for i in df["Scientific name"]
    ]
    return df
