"""Bionty: mapping and standardizing biological entities.

Import the package::

   import bionty as bt

This is the complete API reference:

Entity collections:

.. autosummary::
   :toctree: .

   species

Entity classes:

.. autosummary::
   :toctree: .

   Celltype
   Disease
   Gene
   Protein
   Species
   Tissue

Other tools:

.. autosummary::
   :toctree: .

   Ontology
"""

from . import _version

__version__ = "0.1a1"

# bio entities
from .gene import Gene
from .protein import Protein
from .species import species, Species
from .celltype import Celltype
from .disease import Disease
from .tissue import Tissue

# tools
from ._normalize import NormalizeColumns
from ._ontology import Ontology
