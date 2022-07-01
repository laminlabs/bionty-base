from typing import Iterable

import pandas as pd

from . import Gene
from ._logging import logger as logg


def check_if_index_compliant(index: Iterable, column, **kwargs):
    """The index already theoretically conforms with the Bionty ID for the entity.

    Meaning, the name of the index column is, for instance `hgnc_symbol`.

    Hence, this function only checks whether the terms in the index are all
    contained in the Bionty ID vocabulary.

    It returns a `pd.Index` of terms that aren't contained in the reference.
    """
    if not isinstance(index, pd.Index):
        input_index = pd.Index(index)
    else:
        input_index = index  # type: ignore

    ref_index = Gene(**kwargs).df.reset_index()[column]

    matches = input_index.isin(
        ref_index
    )  # boolean vector indicating standardized terms

    if all(matches) is True:
        return True
    else:
        return input_index[~matches]


def get_compliant_index_from_column(
    df: pd.DataFrame, column: str, *, keep_data=True, **kwargs
):
    """Get a reference-ID-compliant index based on a column with an alternative identifier.

    Example:
    >>> compliant_index = map_index_from_column(df, "ensemble_id")
    >>> df.index = compliant_index

    This will fail for some entries if the column is not uniquely mappable to
    the Bionty ID.

    There are two options for the user:
    1. Maintain previous index identifiers for the terms that aren't mappable
       and flag them (`keep_data == True`)
    2. Reduce the dimensions to the ones that are mappable (`keep_data == False`)

    Args:
        df: DataFrame with an index different from reference ID, but with a
            column that has mappable information, like an ensemble_id.
        column: Column to be mapped to reference ID.
        keep_data: Keep terms that are not mappable to the reference ID.
    """
    gene = Gene(**kwargs).df
    lookup_index = pd.Index(gene.reset_index()[column])

    lookup_df = pd.DataFrame(index=lookup_index, data={"bionty_id": gene.index})

    # this will fail if there are typos
    # need to think about warning flags and soft implementations of this
    unmatched = check_if_index_compliant(df[column].values, column)

    mapped_index = pd.Index(  # type:ignore
        []
    )  # smart semi-compliant index definition
    if isinstance(unmatched, bool):
        # everything is mappable
        mapped_index = lookup_df.loc[df[column]].index
        integrity = 1.0
    elif len(unmatched) == len(df[column]):
        # not mappable
        integrity = 0.0
        logg.warning("The input column is not mappable to the bionty reference!")
    else:
        # partially mappable
        # number_of_mappable_compliant_terms/total_number_of_terms
        integrity = 1 - len(unmatched) / len(df[column])
        perct_map = integrity * 100
        logg.warning(f"Only {perct_map:.2f} of terms are mappable!")

    return mapped_index, perct_map
