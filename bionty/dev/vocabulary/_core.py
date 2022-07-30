from collections import namedtuple
from functools import cached_property

from ... import CellType, Disease, Species

FEATURES = ["gene", "protein"]


class FeatureModel:
    def __init__(self) -> None:
        pass

    @cached_property
    def lookup(self):
        values = {i: i for i in FEATURES}
        nt = namedtuple("feature", values.keys())

        return nt(**values)


feature_model = FeatureModel().lookup
species = Species().lookup
cell_type = CellType().lookup
disease = Disease().lookup
