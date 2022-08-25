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
   Disease

Lookup of vocabulary:

.. autosummary::
   :toctree: .

   lookup

"""

__version__ = "0.1.11"


# dynamic classes
from ._gene import Gene
from ._species import Species
from ._protein import Protein
from ._celltype import CellType
from ._disease import Disease

# tools
from ._normalize import NormalizeColumns
from ._table import EntityTable
from ._ontology import Ontology
from ._lookup import lookup
