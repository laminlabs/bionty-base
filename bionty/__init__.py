"""Bionty: mapping and standardizing biological entities.

Import the package::

   import bionty as bt

This is the complete API reference:

.. autosummary::
   :toctree: .

   Gene
   Protein
   Taxon
"""

from . import _version

__version__ = _version.get_versions()["version"]

# bio entities
from .gene import Gene
from .protein import Protein
from .taxon import Taxon

# normalizer
from ._normalize import NormalizeColumns
