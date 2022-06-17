from typing import Any, NamedTuple

from .._models import Entity, create_model
from .object import Gene


def create_gene_model(std_id="hgnc_symbol", species="human", **kwargs):
    """Create the gene data model with pydantic.

    Args:
        std_id: the field used as standardized id
        **kwargs: see `_models.create_model`

    Returns:
        `GeneData` data model with each gene as a namedtuple entry
    """
    model = create_model("GeneData", __base__=Entity, **kwargs)
    model.add_fields(**{"species": species})
    df = Gene(species=species).reference
    df.columns = df.columns.str.replace(".", "_", regex=True)
    df = df.loc[:, df.columns.isin(Entry.__annotations__.keys())].copy()
    for i in df.index:
        entry = {}
        entry.update({col: df.loc[i][col] for col in df.columns})
        model.add_fields(**{df.loc[i][std_id]: (Entry, Entry(**entry))})
    return model


class Entry(NamedTuple):
    hgnc_symbol: str
    hgnc_id: str
    name: str
    locus_group: str
    alias_symbol: str
    location: str
    entrez_gene_id: str
    ensembl_gene_id: str
    uniprot_ids: str
    pubmed_id: str


GeneDataModel: Any = create_gene_model()


class GeneModel(GeneDataModel):
    def __call__(self, **kwargs):
        return Gene(**kwargs)


gene = GeneModel(**{"name": "gene", "std_id": "hgnc_symbol"})
