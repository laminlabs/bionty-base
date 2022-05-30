"""Bionty: mapping and standardizing biological entities.

Import the package::

   import bionty as bt

This is the complete API reference:

.. autosummary::
   :toctree: .

   Gene
   Protein
   Taxon
   Celltype
"""

from . import _version

__version__ = _version.get_versions()["version"]

# bio entities
from .gene import Gene
from .protein import Protein
from .taxon import Taxon
from .celltype import Celltype

# normalizer
from ._normalize import NormalizeColumns
