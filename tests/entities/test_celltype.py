import pandas as pd

import bionty as bt


def test_cl_celltype_inspect_name():
    df = pd.DataFrame(
        index=[
            "Boettcher cell",
            "bone marrow cell",
            "interstitial cell of ovary",
            "pancreatic ductal cell",
            "This cell type does not exist",
        ]
    )

    ct = bt.CellType(source="cl", version="2023-04-20")
    inspected_df = ct.inspect(df.index, field=ct.name, return_df=True)

    inspect = inspected_df["__mapped__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, True, True, False])

    assert inspect.equals(expected_series)
