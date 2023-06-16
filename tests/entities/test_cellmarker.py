import pandas as pd

import bionty as bt


def test_cellmarker_cellmarker_inspect_name_human():
    df = pd.DataFrame(
        index=["CCR7", "CD69", "CD8", "CD45RA", "This protein does not exist"]
    )

    cm = bt.CellMarker(source="cellmarker", version="2.0")
    curated = cm.inspect(df.index, field=cm.name)

    assert curated == {
        "mapped": ["CCR7", "CD69", "CD8", "CD45RA"],
        "not_mapped": ["This protein does not exist"],
    }


def test_cellmarker_cellmarker_inspect_name_mouse():
    df = pd.DataFrame(
        index=["Tcf4", "Cd36", "Cd34", "Lgr6", "This protein does not exist"]
    )

    cm = bt.CellMarker(source="cellmarker", version="2.0", species="mouse")
    inspected_df = cm.inspect(df.index, field=cm.name, return_df=True)

    inspect = inspected_df["__mapped__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, True, True, False])

    assert inspect.equals(expected_series)
