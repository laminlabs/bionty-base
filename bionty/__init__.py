"""Bionty: mapping and standardizing biological entities.

Import the package::

   import bionty as bt

This is the complete API reference:

Base models: base entity managers.

.. autosummary::
   :toctree: .

   Table

Standardize indexes:

.. autosummary::
   :toctree: .

   check_if_index_compliant
   get_compliant_index_from_column


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
from .protein import Protein
from .celltype import CellType
from .disease import Disease

# tools
from ._normalize import NormalizeColumns
from ._table import Table
from ._fix_index import check_if_index_compliant, get_compliant_index_from_column
