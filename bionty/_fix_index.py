from typing import Iterable

import pandas as pd

from ._logging import logger as logg


def check_if_index_compliant(index: Iterable):
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
    from bionty import Gene

    ref_index = Gene().df.index
    matches = input_index.isin(
        ref_index
    )  # boolean vector indicating standardized terms

    if len(input_index[matches]) == 0:
        return True
    else:
        return input_index[~matches]


def get_compliant_index_from_column(df: pd.DataFrame, column: str, *, keep_data=True):
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
    from bionty import Gene

    gene = Gene().df
    lookup_index = pd.Index(gene[column])

    lookup_df = pd.DataFrame(index=lookup_index, bionty_id=gene.index)

    # this will fail if there are typos
    # need to think about warning flags and soft implementations of this
    everything_is_mappable = True
    partially_mappable = True

    if everything_is_mappable:
        mapped_index = lookup_df[df[column]]["bionty_id"]
        integrity = "1"
    elif partially_mappable:
        mapped_index = (  # type:ignore
            pd.Index()
        )  # smart semi-compliant index definition
        integrity = "number_of_mappable_compliant_terms/total_number_of_terms"
        logg.warning(f"{integrity}")
    else:
        # not_mappable
        mapped_index = "index"
        integrity = "0"
        logg.warning("...")

    return mapped_index, integrity
