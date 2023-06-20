from typing import Literal, Optional

from .._bionty import Bionty
from ._shared_docstrings import _doc_params, doc_entites


@_doc_params(doc_entities=doc_entites)
class Phenotype(Bionty):
    """Phenotype.

    1. Human Phenotype Ontology
    Edits of terms are coordinated and reviewed on:
    https://hpo.jax.org/app/

    2. Mammalian Phenotype Ontology
    Edits of terms are coordinated and reviewed on:
    https://github.com/mgijax/mammalian-phenotype-ontology

    3. Zebrafish Phenotype Ontology
    Edits of terms are coordinated and reviewed on:
    https://github.com/obophenotype/zebrafish-phenotype-ontology

    Args:
        {doc_entities}
    """

    def __init__(
        self,
        species: str = None,
        source: Optional[Literal["hp", "mp", "zp"]] = None,
        version: Optional[str] = None,
        **kwargs
    ) -> None:
        super().__init__(
            source=source,
            version=version,
            species=species,
            include_id_prefixes={
                "hp": ["HP"],
                "mp": ["MP"],  # mp might require an exclusion prefix for mpath
                "zp": ["ZP"],
            },
            **kwargs
        )
