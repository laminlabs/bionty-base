import typing
from functools import cached_property
from typing import Iterable, Literal, Optional

import pandas as pd

from .._io import loads_pickle
from .._models import BaseModel, create_model
from .._normalize import NormalizeColumns
from .._settings import (
    check_datasetdir_exists,
    check_dynamicdir_exists,
    format_into_dataframe,
    settings,
)
from ..species import Species as SP
from ._query import Biomart, Mygene

_IDs = Literal["ensembl.gene_id", "entrez.gene_id"]
_HGNC = "http://ftp.ebi.ac.uk/pub/databases/genenames/hgnc/tsv/hgnc_complete_set.txt"

GeneData = create_model("GeneData", __module__=__name__)


class Entry(BaseModel):
    hgnc_symbol: str
    hgnc_id: str
    name: str
    locus_group: str
    alias_symbol: str
    location: str
    entrez_gene_id: str
    ensembl_gene_id: str
    uniprot_ids: str


class Gene:
    """Gene.

    Biotypes: https://useast.ensembl.org/info/genome/genebuild/biotypes.html
    Gene Naming: https://useast.ensembl.org/info/genome/genebuild/gene_names.html

    """

    def __init__(self, species="human", biomart=False):
        self._species = SP(common_name=species)
        self._dataclasspath = (
            settings.dynamicdir / f"genedata_{self.species.std_name}.pkl"
        )
        self._ref = None
        self._biomart = biomart

    @property
    def species(self):
        """Bionty.species()."""
        return self._species

    @property
    def std_id(self):
        """The standardized symbol attribute name."""
        STD_ID_DICT = {"human": "hgnc_symbol", "mouse": "mgi_symbol"}
        return STD_ID_DICT[self.species.std_name]

    @property
    def fields(self):
        ATTR_DICT = {"human": ["hgnc_id", "hgnc_symbol"], "mouse": ["mgi_symbol"]}
        return list(typing.get_args(_IDs)) + ATTR_DICT[self.species.std_name]

    @property
    def dataclasspath(self):
        """Path to the picked dataclass."""
        return self._dataclasspath

    @property
    def biomart(self):
        """Whether to pull reference via the biomart API."""
        return self._biomart

    @cached_property
    def reference(self):
        """Gene reference table."""
        self._pull_ref()
        return self._ref

    @cached_property
    def dataclass(self):
        return self._load_dataclass()

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
        """Create the gene data model with pydantic."""
        df = self.reference.fillna("")
        df.columns = df.columns.str.replace(".", "_", regex=True)
        df["entrez_gene_id"] = (
            df["entrez_gene_id"].astype(str).str.replace(".0", "", regex=False)
        )
        df = df.loc[:, df.columns.isin(Entry.__annotations__.keys())].copy()
        for i in df.index:
            entry = {}
            entry.update({col: df.loc[i][col] for col in df.columns})
            GeneData.add_fields(**{df.loc[i][self.std_id]: (Entry, Entry(**entry))})

        return GeneData

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
            mapped_dict = self.search(
                data.index, id_type_from=id_type, id_type_to=self.std_id
            )

        data["std_id"] = data.index.map(mapped_dict)
        if new_index:
            data["index_orig"] = data.index
            data.index = data["std_id"].fillna(data["index_orig"])
            data.index.name = None

        if _reformat:
            return data

    def search(
        self,
        genes: Iterable[str],
        id_type_from="ensembl_gene_id",
        id_type_to=None,
    ):
        """Search among fields that are in the `.reference` table.

        Args:
            genes: Input list
            id_type_from: ID type of the input list, see `.attributes`
            id_type_to: ID type to convert into
                Default is the `.std_id`

        Returns:
            a dict of mapped ids
        """
        # default if to convert tp the standardized id
        if id_type_to is None:
            id_type_to = self.std_id

        # get mappings from the reference table
        df = self.reference.reset_index().set_index(id_type_from)[[id_type_to]].copy()

        return df[df.index.isin(genes)].to_dict()[id_type_to]

    def _pull_ref(self):
        """Pulling gene reference table.

        If biomart, pull the reference table from biomart
        If not, pull the reference table from HGNC directly
        """
        if self.biomart:
            ref = Biomart().get_gene_ensembl(species=self.species.std_name)
            if "entrezgene_id" in ref.columns:
                ref["entrezgene_id"] = (
                    ref["entrezgene_id"]
                    .fillna(0)
                    .astype(int)
                    .astype(object)
                    .where(ref["entrezgene_id"].notnull())
                )
            self._ref = ref
        else:
            self._ref = self.hgnc(species=self.species.std_name)

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
        mapped_dict = self.search(df.index, "hgnc_symbol", "hgnc_id")
        mapped_dict.update({k: k for k in mapped_dict.keys()})

        # 2. For not mapped symbols, map through alias
        notmapped = df[~df.index.isin(mapped_dict.keys())].copy()
        if notmapped.shape[0] > 0:
            mg = Mygene()
            res = mg.query(
                notmapped.index, scopes="symbol,alias", species=self.species.std_name
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
        udf["std_id"] = udf["hgnc_id"].map(
            self.search(udf["hgnc_id"], "hgnc_id", "hgnc_symbol")
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
                d = self.search(hids, "hgnc_id", "hgnc_symbol")
                mapped_dict[dup] = pd.DataFrame.from_dict(d, orient="index")[0].min()

        return mapped_dict

    @check_datasetdir_exists
    def hgnc(self, species="human"):
        """HGNC symbol from the HUGO Gene Nomenclature Committee."""
        if species != "human":
            raise AssertionError("HGNC is only for human!")

        filepath = settings.datasetdir / "hgnc_complete_set.txt"
        if not filepath.exists():
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
        NormalizeColumns.gene(df, species=species)

        return df
