"""Bionty.

Import the package::

   import bionty as bt

Entities:

.. autosummary::
   :toctree: .

   Organism
   Gene
   Protein
   CellMarker
   CellType
   CellLine
   Tissue
   Disease
   Phenotype
   Pathway
   ExperimentalFactor
   DevelopmentalStage
   Drug
   Ethnicity
   BFXPipeline
   BioSample

Base model of entity classes:

.. autosummary::
   :toctree: .

   Bionty
   BiontyField

Bionty sources:

.. autosummary::
   :toctree: .

    display_available_sources
    display_currently_used_sources
    reset_sources
    settings

External API:

.. autosummary::
   :toctree: .

   Ontology
"""

__version__ = "0.35.2"  # denote release candidate for 0.1.0 with 0.1rc1

# prints warning of python versions
from lamin_utils import py_version_warning

py_version_warning("3.8", "3.10")

from ._sync_sources import sync_sources

sync_sources()

# dynamic classes
from . import dev

# tools
from ._bionty import Bionty, BiontyField
from ._display_sources import display_available_sources, display_currently_used_sources
from ._ontology import Ontology
from ._settings import settings

# sources
from .dev._handle_sources import reset_sources
from .entities._bfxpipeline import BFXPipeline
from .entities._biosample import BioSample
from .entities._cellline import CellLine
from .entities._cellmarker import CellMarker
from .entities._celltype import CellType
from .entities._developmentalstage import DevelopmentalStage
from .entities._disease import Disease
from .entities._drug import Drug
from .entities._ethnicity import Ethnicity
from .entities._experimentalfactor import ExperimentalFactor
from .entities._gene import Gene
from .entities._organism import Organism
from .entities._pathway import Pathway
from .entities._phenotype import Phenotype
from .entities._protein import Protein
from .entities._tissue import Tissue

# backward compat
Entity = Bionty
Readout = ExperimentalFactor
Species = Organism
