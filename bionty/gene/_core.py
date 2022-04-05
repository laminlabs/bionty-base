from typing import Optional, Literal, Iterable
import pandas as pd
from ..species import Species
from .._settings import settings
from ._query import Biomart, Mygene

_IDs = Optional[Literal["ensembl_gene_id", "entrezgene_id", "uniprot_gn_id"]]
_HGNC = "http://ftp.ebi.ac.uk/pub/databases/genenames/hgnc/tsv/hgnc_complete_set.txt"


class Gene:
    """Gene

    Biotypes: https://useast.ensembl.org/info/genome/genebuild/biotypes.html
    Gene Naming: https://useast.ensembl.org/info/genome/genebuild/gene_names.html

    """

    def __init__(self, species="human"):
        self._species = Species(species=species)
        self._pull_ref()

    @property
    def species(self):
        """biomap.bioentity.Species"""
        return self._species

    @property
    def reference(self):
        """Gene reference table"""
        return self._ref

    @property
    def std_id(self):
        """The standardized symbol attribute name"""
        std_id_dict = {"human": "hgnc_symbol", "mouse": "mgi_symbol"}
        return std_id_dict[self.species.common_name]

    def standardize(
        self,
        data: Iterable[str],
        id_type: _IDs = None,
        new_index: bool = True,
    ):
        """Index a dataframe with the official gene symbols from HGNC

        Parameters
        ----------
        data
            A list of gene symbols to be standardized
            If dataframe, will take the index
        id_type
            Default is to consider input as gene symbols and alias
            The other options are ['ensembl_id', 'entrez_id', 'uniprot_id', 'hgnc_id']
        new_index
            If True, set the standardized symbols as the index
                - unmapped will remain the original index
                - original index stored in the `index_orig` column
            If False, write to the `standardized_symbol` column

        Returns
        -------
        Replaces the DataFrame mappable index with the standardized symbols
        Adds a `std_id` column
        The original index is stored in the `index_orig` column
        """

        df = self._format(data)

        if id_type is None:
            mapped_dict = self._standardize_symbol(df=df)
        else:
            mapped_dict = self.get_attribute(
                df.index, id_type_from=id_type, id_type_to=self.std_id
            )

        df["std_id"] = df.index.map(mapped_dict)
        if new_index:
            df["index_orig"] = df.index
            df.index = df["std_id"].fillna(df["index_orig"])
            df.index.name = None

    def get_attribute(
        self,
        genes: Iterable[str],
        id_type_from: _IDs = "hgnc_id",
        id_type_to: _IDs = "hgnc_symbol",
    ):
        """Convert among IDs that are in the `.reference` table

        Parameters
        ----------
        genes
            Input list
        id_type_from
            ID type of the input list
        id_type_to
            ID type to convert into

        Returns
        -------
        a dict of mapped ids
        """
        df = self.reference.reset_index().set_index(id_type_from)[[id_type_to]].copy()
        return df[df.index.isin(genes)].to_dict()[id_type_to]

    def _pull_ref(self):
        """Pulling gene reference table"""
        self._ref = Biomart().get_gene_ensembl(species=self.species.common_name)

    def _standardize_symbol(
        self,
        df: pd.DataFrame,
    ):
        """Standardize gene symbols/aliases to symbol from `.reference` table

        Parameters
        ----------
        df
            A dataframe with index being the column to be standardized
        species
            'human'

        Returns
        -------
        a dict with the standardized symbols
        """

        # 1. Mapping from symbol to hgnc_id using .hgnc table
        mapped_dict = self.get_attribute(df.index, "hgnc_symbol", "hgnc_id")
        mapped_dict.update({k: k for k in mapped_dict.keys()})

        # 2. For not mapped symbols, map through alias
        notmapped = df[~df.index.isin(mapped_dict.keys())].copy()
        if notmapped.shape[0] > 0:
            mg = Mygene()
            res = mg.querymany(
                notmapped.index, scopes="symbol,alias", species=self.species.common_name
            )
            mapped_dict.update(self._cleanup_mygene_returns(res))

        return mapped_dict

    def _cleanup_mygene_returns(self, res: pd.DataFrame, unique_col="hgnc_id"):
        """Clean up duplicates and NAs from the mygene returns

        Parameters
        ----------
        res
            Returned dataframe from `.mg_querymany`
        unique_col
            Unique identifier column

        Returns
        -------
        a dict with only uniquely mapped IDs
        """
        mapped_dict = {}

        # drop columns without mapped unique IDs (HGNC)
        df = res.dropna(subset=unique_col)

        # for unique results, use returned HGNC IDs to get symbols from .hgnc
        udf = df[~df.index.duplicated(keep=False)].copy()
        udf["std_id"] = udf["hgnc_id"].map(
            self.get_attribute(udf["hgnc_id"], "hgnc_id", "hgnc_symbol")
        )
        mapped_dict.update(udf[["std_id"]].to_dict()["std_id"])

        # TODO: if the same HGNC ID is mapped to multiple inputs?
        if df[unique_col].duplicated().sum() > 0:
            pass

        # if a query is mapped to multiple HGNC IDs, do the reverse mapping from .hgnc
        # keep the shortest symbol as readthrough transcripts or pseudogenes are longer
        if df.index.duplicated().sum() > 0:
            dups = df[df.index.duplicated(keep=False)].copy()
            for dup in dups.index.unique():
                hids = dups[dups.index == dup][unique_col].tolist()
                d = self.get_attribute(hids, "hgnc_id", "hgnc_symbol")
                mapped_dict[dup] = pd.DataFrame.from_dict(d, orient="index")[0].min()

        return mapped_dict

    def _dataframe(self, data: Iterable[str]):
        """Format the input into the index of a dataframe"""
        if not isinstance(data, pd.DataFrame):
            df = pd.DataFrame(index=[d for d in data])
        else:
            df = data
        return df

    def _format(self, data: Iterable[str]):
        """Adding columns to a dataframe for standardization"""
        df = self._dataframe(data)
        return df

    @classmethod
    def attributes(cls, species="human"):
        shared = [
            "ensembl_gene_id",
            "entrezgene_id",
            "uniprot_gn_id",
        ]
        attr_dict = {"human": ["hgnc_id", "hgnc_symbol"], "mouse": ["mgi_symbol"]}
        return shared + attr_dict[species]

    @classmethod
    def HGNC(cls, species="human"):
        """HGNC symbol from the HUGO Gene Nomenclature Committee"""
        if species != "human":
            raise AssertionError("HGNC is only for human!")

        filepath = settings.datasetdir / "hgnc_complete_set.txt"
        filepath.parent.mkdir(exist_ok=True)
        if not filepath.exists():
            from urllib.request import urlretrieve

            urlretrieve(_HGNC, filepath)
        return pd.read_csv(
            filepath,
            sep="\t",
            index_col=0,
            low_memory=False,  # If True, gets DtypeWarning
            verbose=False,
        )
