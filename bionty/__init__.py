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

__version__ = "0.1.3"


# dynamic classes
from ._gene import Gene
from ._species import Species, species
from ._protein import Protein
from ._celltype import CellType, cell_type
from ._disease import Disease, disease

# tools
from ._normalize import NormalizeColumns
from ._table import EntityTable
