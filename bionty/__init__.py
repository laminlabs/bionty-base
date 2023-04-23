"""Bionty: Data model generator for biology.

Import the package::

   import bionty as bt

Entities:

.. autosummary::
   :toctree: .

   Gene
   Protein
   Species
   CellLine
   CellType
   CellMarker
   Tissue
   Disease
   Phenotype
   Pathway
   Readout

The base model for every entity class is:

.. autosummary::
   :toctree: .

   Entity

Display of currently available or used versions:

.. autosummary::
   :toctree: .

    display_available_versions
    display_active_versions

Lookup of vocabulary:

.. autosummary::
   :toctree: .

   lookup

Setting default ontologies

.. autosummary::
    :toctree: .

    update_defaults

External API:

.. autosummary::
   :toctree: .

   Ontology

Dev API:

.. autosummary::
   :toctree: .

   dev

"""

__version__ = "0.11.6"  # denote release candidate for 0.1.0 with 0.1rc1

# prints warning of python versions
from lamin_logger import py_version_warning

py_version_warning("3.8", "3.10")

from . import _sync_versions
from ._sync_versions import update_defaults

# dynamic classes
from .entities._gene import Gene
from .entities._species import Species
from .entities._protein import Protein
from .entities._cellline import CellLine
from .entities._celltype import CellType
from .entities._cellmarker import CellMarker
from .entities._tissue import Tissue
from .entities._disease import Disease
from .entities._phenotype import Phenotype
from .entities._pathway import Pathway
from .entities._readout import Readout

# tools
from ._normalize import NormalizeColumns
from ._entity import Entity
from ._ontology import Ontology
from ._lookup import lookup
from ._display_versions import display_active_versions, display_available_versions

# dev
from . import dev
