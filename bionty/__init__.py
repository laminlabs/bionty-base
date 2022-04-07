"""Bionty: mapping and standardizing biological entities.."""

from . import _version

__version__ = _version.get_versions()["version"]

# bio entities
from . import taxon, gene, protein

# normalizer
from ._normalize import NormalizeColumns
