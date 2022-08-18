from collections import namedtuple
from typing import Iterable

from ... import CellType, Disease, Species
from ..._normalize import GENE_COLUMNS

FEATURES = ["gene", "protein"]


def lookup(values: Iterable[str]):
    """Look up a list of values via tab completion."""
    nt = namedtuple("feature", values)  # type: ignore
    return nt(**{i: i for i in values})


feature_model = lookup(values=FEATURES)
gene_id = lookup(values=set(GENE_COLUMNS.values()))
species = Species().lookup
cell_type = CellType().lookup
disease = Disease().lookup
