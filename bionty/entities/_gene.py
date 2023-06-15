from typing import Literal, Optional, Tuple, Union

import pandas as pd

from .._bionty import Bionty, BiontyField
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

    def lookup(self, field: Union[BiontyField, str] = "symbol") -> Tuple:
        """Return an auto-complete object for the bionty field.

        Args:
            field: The field to lookup the values for.
                   Defaults to 'name'.

        Returns:
            A NamedTuple of lookup information of the field values.

        Examples:
            >>> import bionty as bt
            >>> gene_lookout = bt.Gene().lookup()
            >>> gene_lookout.TEF
        """
        return super().lookup(field=field)

    def search(
        self,
        string: str,
        field: Union[BiontyField, str] = "symbol",
        synonyms_field: Union[BiontyField, str, None] = "synonyms",
        case_sensitive: bool = True,
        return_ranked_results: bool = False,
    ) -> pd.DataFrame:
        """Fuzzy matching of a given string against a Bionty field.

        Args:
            string: The input string to match against the field ontology values.
            field: The BiontyField of ontology the input string is matching against.
            synonyms_field: Also map against in the synonyms (If None, no mapping against synonyms).
            case_sensitive: Whether the match is case sensitive.
            return_ranked_results: Whether to return all entries ranked by matching ratios.

        Returns:
            Best match of the input string.

        Examples:
            >>> import bionty as bt
            >>> celltype_bionty = bt.CellType()
            >>> celltype_bionty.search("gamma delta T cell", celltype_bionty.name)
        """
        return super().search(
            string=string,
            field=field,
            synonyms_field=synonyms_field,
            case_sensitive=case_sensitive,
            return_ranked_results=return_ranked_results,
        )
