"""Bionty: mapping and standardizing biological entities.

Import the package::

   import bionty as bt

The base model for every entity class is:

.. autosummary::
   :toctree: .

   EntityTable

Entities:

.. autosummary::
   :toctree: .

   Species
   Gene
   Protein
   CellType
   CellMarker
   Disease

Lookup of vocabulary:

.. autosummary::
   :toctree: .

   lookup

"""

__version__ = "0.2.0"


# dynamic classes
from ._gene import Gene
from ._species import Species
from ._protein import Protein
from ._celltype import CellType
from ._cellmarker import CellMarker
from ._disease import Disease

# tools
from ._normalize import NormalizeColumns
from ._table import EntityTable
from ._ontology import Ontology
from ._lookup import lookup
