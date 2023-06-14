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


def explode_aggregated_column_to_expand(
    df: pd.DataFrame,
    aggregated_col: str,
    target_col=None,
    sep: str = "|",
) -> pd.DataFrame:
    """Explode values from an aggregated DataFrame column to expand a target column.

    Args:
        df: A DataFrame containing the aggregated_col and target_col.
        aggregated_col: The name of the aggregated column
        target_col: the name of the target column
                    If None, use the index as the target column
        sep: Splits all values of the aggregated_col by this separator.

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
    if aggregated_col == target_col:
        raise AssertionError("synonyms and target columns can't be the same!")
    try:
        df = df.reset_index()[[aggregated_col, target_col]].copy()
    except KeyError:
        raise KeyError(f"{aggregated_col} field is not found!")

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
    df_concat = df_concat.astype(str)
    df_concat = df_concat.groupby(aggregated_col).agg(sep.join)

    return df_concat
