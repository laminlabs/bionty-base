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

Developer API:

.. autosummary::
   :toctree: .

   dev

"""

__version__ = "0.1.1"


# dynamic classes
from .gene import Gene
from .species import Species
from .protein import Protein
from .celltype import CellType
from .disease import Disease

# tools
from ._normalize import NormalizeColumns
from ._table import EntityTable
