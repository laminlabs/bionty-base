from collections import namedtuple
from typing import Iterable

from ._normalize import GENE_COLUMNS, PROTEIN_COLUMNS
from ._readout import Readout
from ._species import Species


def _lookup(values: Iterable[str]):
    """Look up a list of values via tab completion."""
    nt = namedtuple("feature", values)  # type: ignore
    return nt(**{i: i for i in values})


class lookup:
    """Look up a list of values via tab completion."""

    gene_id = _lookup(values=set(GENE_COLUMNS.values()))
    protein_id = _lookup(values=set(PROTEIN_COLUMNS.values()))
    species = Species().lookup
    readout = Readout().lookup
