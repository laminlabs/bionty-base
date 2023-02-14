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
   Readout

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

Dev API:

.. autosummary::
   :toctree: .

   dev

"""

__version__ = "0.7.0"

# prints warning of python versions
from lamin_logger import py_version_warning

py_version_warning("3.7", "3.10")

from . import _sync_versions

# dynamic classes
from ._gene import Gene
from ._species import Species
from ._protein import Protein
from ._celltype import CellType
from ._cellmarker import CellMarker
from ._tissue import Tissue
from ._disease import Disease
from ._phenotype import Phenotype
from ._readout import Readout

# tools
from ._normalize import NormalizeColumns
from ._table import EntityTable
from ._ontology import Ontology
from ._lookup import lookup

# dev
from . import dev
