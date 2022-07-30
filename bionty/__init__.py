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

__version__ = "0.1.4"


# dynamic classes
from ._gene import Gene
from ._species import Species
from ._protein import Protein
from ._celltype import CellType
from ._disease import Disease

# tools
from ._normalize import NormalizeColumns
from ._table import EntityTable

# dev
from .dev import vocabulary
