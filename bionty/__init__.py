"""Bionty: mapping and standardizing biological entities.

Import the package::

   import bionty as bt

This is the complete API reference:

Base models: base entity managers.

.. autosummary::
   :toctree: .

   Ontology

Entity classes: dynamic classes of entities.

.. autosummary::
   :toctree: .

   CellType
   Disease
   Gene
   Protein
   Species
   Tissue

Entity collections: static classes of entities.

.. autosummary::
   :toctree: .

   gene
   species
"""

from . import _version

__version__ = "0.1a3"


# dynamic classes
from .gene import Gene
from .protein import Protein
from .species import Species
from .celltype import CellType
from .disease import Disease
from .tissue import Tissue

# tools
from ._normalize import NormalizeColumns
from ._ontology import Ontology
