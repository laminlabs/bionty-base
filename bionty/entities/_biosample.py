from typing import Literal, Optional

from .._bionty import Bionty
from ._shared_docstrings import _doc_params, doc_entites


@_doc_params(doc_entities=doc_entites)
class BioSample(Bionty):
    """BioSample attributes.

    1. NCBI BioSample Attributes
    https://www.ncbi.nlm.nih.gov/biosample/docs/attributes

    Args:
        {doc_entities}
    """

    def __init__(
        self,
        organism: Optional[Literal["all"]] = None,
        source: Optional[Literal["ncbi"]] = None,
        version: Optional[str] = None,
        **kwargs
    ) -> None:
        super().__init__(source=source, version=version, organism=organism, **kwargs)
