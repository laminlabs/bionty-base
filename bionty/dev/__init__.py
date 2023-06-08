"""Developer API.

.. autosummary::
   :toctree: .

   ontology_info
"""
from ._fix_index import (
    check_if_index_compliant,
    get_compliant_index_from_column,
    explode_aggregated_column_to_expand,
)  # noqa

from ._ontology import ontology_info
