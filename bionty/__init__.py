"""Bionty: mapping and standardizing biological entities.

Import the package::

   import bionty as bt

This is the complete API reference:

Base models: base entity managers.

.. autosummary::
   :toctree: .

   Table

Entity classes: dynamic classes of entities.

.. autosummary::
   :toctree: .

   Species
   Gene
   CellType
   Disease

"""

__version__ = "0.1.0"


# dynamic classes
from .gene import Gene
from .species import Species
from .celltype import CellType
from .disease import Disease

# tools
from ._normalize import NormalizeColumns
from ._table import Table
