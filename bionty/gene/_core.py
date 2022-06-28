from collections import namedtuple
from functools import cached_property
from typing import Literal, Optional

import pandas as pd

from .._normalize import NormalizeColumns
from .._settings import check_datasetdir_exists, format_into_dataframe, settings
from ._query import Mygene

_IDs = Literal["ensembl.gene_id", "entrez.gene_id"]
_HGNC = "https://bionty-assets.s3.amazonaws.com/hgnc_complete_set.txt"


STD_ID_DICT = {"human": "hgnc_symbol", "mouse": "mgi_symbol"}
ATTR_DICT = {"human": ["hgnc_id", "hgnc_symbol"], "mouse": ["mgi_symbol"]}


class Gene:
    """Gene.

    Args:
        id: If `None`, chooses an id field in a species dependent way.
        species: `common_name` of `Species` entity table.

    Notes:
        Biotypes: https://useast.ensembl.org/info/genome/genebuild/biotypes.html
        Gene Naming: https://useast.ensembl.org/info/genome/genebuild/gene_names.html

    """

    def __init__(self, id=None, species="human"):
        self._species = species
        self._id_field = STD_ID_DICT[species]

    @cached_property
    def df(self):
        """DataFrame."""
        if self._species == "human":
            return self._hgnc_human()
        else:
            raise NotImplementedError

    @cached_property
    def lookup(self):
        """Lookup object for auto-complete."""
        values = self.df.index.str.replace("-", "_").str.rstrip("@").to_list()
        return namedtuple("id", values)

    @format_into_dataframe
    def standardize(
        self,
        data,
        id_type: Optional[_IDs] = None,
        new_index: bool = True,
        _reformat: bool = False,
    ):
        """Index a dataframe with the official gene symbols from HGNC.

        Args:
            data: A list of gene symbols to be standardized
                If dataframe, will take the index
            id_type: Default is to consider input as gene symbols and alias
            new_index:
                If True, set the standardized symbols as the index
                    - unmapped will remain the original index
                    - original index stored in the `index_orig` column

                If False, write to the `standardized_symbol` column

        Returns:
            Replaces the DataFrame mappable index with the standardized symbols
            Adds a `std_id` column
            The original index is stored in the `index_orig` column
        """
        if id_type is None:
            mapped_dict = self._standardize_symbol(df=data)
        else:
            NotImplementedError
        data["std_id"] = data.index.map(mapped_dict)
        if new_index:
            data["index_orig"] = data.index
            data.index = data["std_id"].fillna(data["index_orig"])
            data.index.name = None

        if _reformat:
            return data

    def _standardize_symbol(
        self,
        df: pd.DataFrame,
    ):
        """Standardize gene symbols/aliases to symbol from `.reference` table.

        Args:
            df: A dataframe with index being the column to be standardized
            species: 'human'

        Returns:
            a dict with the standardized symbols
        """
        # 1. Mapping from symbol to hgnc_id using .hgnc table
        mapped_dict = self.df.loc[self.df.index.isin(df.index), ["hgnc_id"]].to_dict()[
            "hgnc_id"
        ]
        mapped_dict.update({k: k for k in mapped_dict.keys()})

        # 2. For not mapped symbols, map through alias
        notmapped = df[~df.index.isin(mapped_dict.keys())].copy()
        if notmapped.shape[0] > 0:
            mg = Mygene()
            res = mg.query(
                notmapped.index, scopes="symbol,alias", species=self._species
            )
            mapped_dict.update(self._cleanup_mygene_returns(res))

        return mapped_dict

    def _cleanup_mygene_returns(self, res: pd.DataFrame, unique_col="hgnc_id"):
        """Clean up duplicates and NAs from the mygene returns.

        Args:
            res: Returned dataframe from `.mg.query`
            unique_col: Unique identifier column

        Returns:
            a dict with only uniquely mapped IDs
        """
        mapped_dict = {}

        # drop columns without mapped unique IDs (HGNC)
        df = res.dropna(subset=unique_col)

        # for unique results, use returned HGNC IDs to get symbols from .hgnc
        udf = df[~df.index.duplicated(keep=False)].copy()
        df_ = self.df.reset_index().set_index("hgnc_id")
        udf["std_id"] = udf["hgnc_id"].map(
            df_.loc[df_.index.isin(udf["hgnc_id"]), ["hgnc_symbol"]].to_dict()[
                "hgnc_symbol"
            ]
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
                df_ = self.df.reset_index().set_index("hgnc_id")
                d = df_.loc[df_.index.isin(hids), ["hgnc_symbol"]].to_dict()[
                    "hgnc_symbol"
                ]
                mapped_dict[dup] = pd.DataFrame.from_dict(d, orient="index")[0].min()

        return mapped_dict

    @check_datasetdir_exists
    def _hgnc_human(self):
        """HGNC symbol from the HUGO Gene Nomenclature Committee."""
        filepath = settings.datasetdir / "hgnc_complete_set.txt"
        if not filepath.exists():
            print("retrieving HUGO complete gene set from EBI")
            from urllib.request import urlretrieve

            urlretrieve(_HGNC, filepath)
        df = pd.read_csv(
            filepath,
            sep="\t",
            index_col=0,
            low_memory=False,  # If True, gets DtypeWarning
            verbose=False,
        )
        df = df.reset_index().copy()
        NormalizeColumns.gene(df, species="human")

        df = df.set_index("hgnc_symbol")

        return df
