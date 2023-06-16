from typing import Literal, Optional

from .._bionty import Bionty
from ._shared_docstrings import _doc_params, doc_entites


@_doc_params(doc_entities=doc_entites)
class Gene(Bionty):
    """Gene.

    1. Ensembl
    Edits of terms are coordinated and reviewed on:
    https://www.ensembl.org/

    Args:
        {doc_entities}

    Notes:
        Biotypes: https://www.ensembl.org/info/genome/genebuild/biotypes.html
        Gene Naming: https://www.ensembl.org/info/genome/genebuild/gene_names.html
    """

    def __init__(
        self,
        species: str = "human",
        source: Optional[Literal["ensembl"]] = None,
        version: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(
            source=source,
            version=version,
            species=species,
            **kwargs,
        )
