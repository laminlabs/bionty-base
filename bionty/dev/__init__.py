"""Developer API.

.. autosummary::
   :toctree: .

   check_if_index_compliant
   get_compliant_index_from_column
"""
from ._fix_index import (
    check_if_index_compliant,
    get_compliant_index_from_column,
    explode_aggregated_column_to_expand,
)  # noqa
