import numpy as np
import pandas as pd


def check_if_index_compliant(index: pd.Index, ref_index: pd.Index) -> np.ndarray:
    """The index already theoretically conforms with the Bionty ID for the entity.

    Meaning, the name of the index column is, for instance `hgnc_symbol`.

    Hence, this function only checks whether the terms in the index are all
    contained in the Bionty ID vocabulary.

    It returns a `pd.Index` of terms that aren't contained in the reference.
    """
    # boolean vector indicating standardized terms
    matches = index.isin(ref_index)
    return matches


def get_compliant_index_from_column(
    df: pd.DataFrame,
    ref_df: pd.DataFrame,
    column: str,
):
    """Get a reference-ID-compliant index based on a column with an alternative identifier.

    Example:
    >>> compliant_index = map_index_from_column(df, "ensemble_id")
    >>> df.index = compliant_index

    This will fail for some entries if the column is not uniquely mappable to
    the Bionty ID.

    There are two options for the user:
    1. Maintain previous index identifiers for the terms that aren't
    mappable and flag them (`keep_data == True`)
    2. Reduce the dimensions to the ones that are mappable (`keep_data == False`)

    Args:
        df: DataFrame with an index different from reference ID, but with a
            column that has mappable information, like an ensemble_id.
        ref_df: Reference EntityTable in Bionty.
        column: Column to be mapped to reference ID.
        keep_data: Keep terms that are not mappable to the reference ID.
    """
    df = df.copy()  # not touch the input df

    # prepare ref_df for lookup
    ref_index = ref_df.index
    ref_df = ref_df.reset_index()

    if column not in ref_df.columns:
        raise AssertionError(f"{column} name must match one of {ref_df.columns}!")
    else:
        query_values = df[column].values

    # lookup_df is indexed with the query column field in the ref_df
    # and with a "bionty_id" column containing the Bionty default identifier
    # e.g. default is `hgnc_symbol` for human
    lookup_df = pd.DataFrame(index=ref_df[column], data={"bionty_id": ref_index})

    matches = check_if_index_compliant(pd.Index(query_values), lookup_df.index)

    if all(~matches):  # nothing is mappable
        raise AssertionError(f"{column} name must contain at least one mappable term!")

    # mapped_dict is the {query_id: bionty_id}, where query_id = ref_df[column]
    lookup_df_mappable = lookup_df.loc[query_values[matches]]
    mapper = lookup_df_mappable["bionty_id"]
    mapper = mapper.drop_duplicates()
    new_index = df[column].map(mapper)  # what's unmappable results in nan
    new_index = new_index.fillna(df[column]).values  # fill nans with orig values

    return pd.Index(new_index), matches


def explode_aggregated_column_to_expand(
    df: pd.DataFrame, aggregated_col=str, target_col=None, sep="|"
):
    """Explode values from an aggregated DataFrame column to expand a target column.

    Args:
        df: a DataFrame containing the aggregated_col and target_col
        aggregated_col: the name of the aggregated column
        target_col: the name of the target column
            If None, use the index as the target column

    Returns:
        a DataFrame index by the split values from the aggregated column;
        the target column is aggregated so that the new index is unique.
    """
    if target_col is None:
        # take the index as the target column
        if df.index.name is None:
            target_col = df.index.name = "index"
        else:
            target_col = df.index.name
    df = df.reset_index()[[aggregated_col, target_col]].copy()

    # explode the values from the aggregated cells into new rows
    df[aggregated_col] = df[aggregated_col].str.split(sep)
    exploded_df = df.explode(aggregated_col)

    # if any values in the aggregated column is already in the target col
    # sets those values of the aggregated column to None
    exploded_df.loc[
        exploded_df[aggregated_col].isin(exploded_df[target_col]), aggregated_col
    ] = None

    # set the values aggregated_col equal the target_col if None before concat
    exploded_df[aggregated_col] = exploded_df[aggregated_col].fillna(
        exploded_df[target_col]
    )

    # append the additional values in the target column to the df
    add_values = exploded_df[
        ~exploded_df[target_col].isin(exploded_df[aggregated_col])
    ][target_col].unique()
    add_df = pd.DataFrame(data={target_col: add_values, aggregated_col: add_values})

    # aggregate the target column so that the new index (aggregated column) is unique
    df_concat = pd.concat([exploded_df, add_df])
    df_concat = df_concat.groupby(aggregated_col).agg(sep.join)

    return df_concat
