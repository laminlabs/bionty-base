"""Bionty: mapping and standardizing biological entities.."""

from . import _version

__version__ = _version.get_versions()["version"]

# bio entities
from .gene import Gene
from .protein import Protein
from .taxon import Taxon

# normalizer
from ._normalize import NormalizeColumns
