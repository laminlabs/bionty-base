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

Autolook up shortcuts:

.. autosummary::
   :toctree: .

   species
   cell_type
   disease

Developer API:

.. autosummary::
   :toctree: .

   dev

"""

__version__ = "0.1.2"


# dynamic classes
from .gene import Gene
from .species import Species, species
from .protein import Protein
from .celltype import CellType, cell_type
from .disease import Disease, disease

# tools
from ._normalize import NormalizeColumns
from ._table import EntityTable
