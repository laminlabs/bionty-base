from collections import namedtuple
from typing import Iterable

from ._celltype import CellType
from ._disease import Disease
from ._normalize import GENE_COLUMNS, PROTEIN_COLUMNS
from ._species import Species

FEATURES = ["gene", "protein", "cell_marker"]


def _lookup(values: Iterable[str]):
    """Look up a list of values via tab completion."""
    nt = namedtuple("feature", values)  # type: ignore
    return nt(**{i: i for i in values})


class lookup:
    """Look up a list of values via tab completion."""

    feature_model = _lookup(values=FEATURES)
    gene_id = _lookup(values=set(GENE_COLUMNS.values()))
    protein_id = _lookup(values=set(PROTEIN_COLUMNS.values()))
    species = Species().lookup
    cell_type = CellType().lookup
    disease = Disease().lookup
