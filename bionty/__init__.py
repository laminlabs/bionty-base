"""Bionty: Data model generator for biology.

Import the package::

   import bionty as bt

Entities:

.. autosummary::
   :toctree: .

   Gene
   Protein
   Species
   CellType
   CellMarker
   Tissue
   Disease

The base model for every entity class is:

.. autosummary::
   :toctree: .

   EntityTable

Lookup of vocabulary:

.. autosummary::
   :toctree: .

   lookup

External API:

.. autosummary::
   :toctree: .

   Ontology

"""

__version__ = "0.5.3"


# dynamic classes
from ._gene import Gene
from ._species import Species
from ._protein import Protein
from ._celltype import CellType
from ._cellmarker import CellMarker
from ._tissue import Tissue
from ._disease import Disease

# tools
from ._normalize import NormalizeColumns
from ._table import EntityTable
from ._ontology import Ontology
from ._lookup import lookup
