from functools import cached_property
from typing import Optional, Literal, Iterable
import typing
import pandas as pd
from ..species import Species
from .._settings import settings
from ._query import Biomart, Mygene

_IDs = Literal["ensembl_gene_id", "entrezgene_id"]
_HGNC = "http://ftp.ebi.ac.uk/pub/databases/genenames/hgnc/tsv/hgnc_complete_set.txt"


class Gene:
    """Gene

    Biotypes: https://useast.ensembl.org/info/genome/genebuild/biotypes.html
    Gene Naming: https://useast.ensembl.org/info/genome/genebuild/gene_names.html

    """

    def __init__(self, species="human"):
        self._species = Species(species=species)
        self._ref = None

    @property
    def species(self):
        """Bionty.Species"""
        return self._species

    @property
    def STD_ID(self):
        """The standardized symbol attribute name"""
        STD_ID_DICT = {"human": "hgnc_symbol", "mouse": "mgi_symbol"}
        return STD_ID_DICT[self.species.common_name]

    @property
    def attributes(self):
        ATTR_DICT = {"human": ["hgnc_id", "hgnc_symbol"], "mouse": ["mgi_symbol"]}
        return list(typing.get_args(_IDs)) + ATTR_DICT[self.species.common_name]

    @cached_property
    def reference(self):
        """Gene reference table"""
        self._pull_ref()
        return self._ref

    def standardize(
        self,
        data: Iterable[str],
        id_type: Optional[_IDs] = None,
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
        new_index
            If True, set the standardized symbols as the index
                - unmapped will remain the original index
                - original index stored in the `index_orig` column
            If False, write to the `standardized_symbol` column

        Returns
        -------
        Replaces the DataFrame mappable index with the standardized symbols
        Adds a `STD_ID` column
        The original index is stored in the `index_orig` column
        """

        df = self._format(data)

        if id_type is None:
            mapped_dict = self._standardize_symbol(df=df)
        else:
            mapped_dict = self.get_attribute(
                df.index, id_type_from=id_type, id_type_to=self.STD_ID
            )

        df["STD_ID"] = df.index.map(mapped_dict)
        if new_index:
            df["index_orig"] = df.index
            df.index = df["STD_ID"].fillna(df["index_orig"])
            df.index.name = None

    def get_attribute(
        self,
        genes: Iterable[str],
        id_type_from: Optional[_IDs] = "ensembl_gene_id",
        id_type_to: Optional[_IDs] = None,
    ):
        """Convert among IDs that are in the `.reference` table

        Parameters
        ----------
        genes
            Input list
        id_type_from
            ID type of the input list, see `.attributes`
        id_type_to: str (Default is the `.STD_ID`)
            ID type to convert into

        Returns
        -------
        a dict of mapped ids
        """

        # default if to convert tp the standardized id
        if id_type_to is None:
            id_type_to = self.STD_ID

        # get mappings from the reference table
        df = self.reference.reset_index().set_index(id_type_from)[[id_type_to]].copy()

        return df[df.index.isin(genes)].to_dict()[id_type_to]

    def _pull_ref(self):
        """Pulling gene reference table"""
        ref = Biomart().get_gene_ensembl(species=self.species.common_name)
        if "entrezgene_id" in ref.columns:
            ref["entrezgene_id"] = (
                ref["entrezgene_id"]
                .fillna(0)
                .astype(int)
                .astype(object)
                .where(ref["entrezgene_id"].notnull())
            )
        self._ref = ref

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
        udf["STD_ID"] = udf["hgnc_id"].map(
            self.get_attribute(udf["hgnc_id"], "hgnc_id", "hgnc_symbol")
        )
        mapped_dict.update(udf[["STD_ID"]].to_dict()["STD_ID"])

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
