import pandas as pd

import bionty as bt


def test_cellmarker_cellmarker_curation_name_human():
    df = pd.DataFrame(
        index=["CCR7", "CD69", "CD8A", "CD45RA", "This protein does not exist"]
    )

    cm = bt.CellMarker(source="cellmarker", version="2.0")
    curated_df = cm.curate(df, reference_id=cm.name)

    curation = curated_df["__curated__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, True, True, False])

    assert curation.equals(expected_series)


def test_cellmarker_cellmarker_curation_name_mouse():
    df = pd.DataFrame(
        index=["Tcf4", "Cd36", "Cd34", "Cd45", "This protein does not exist"]
    )

    cm = bt.CellMarker(source="cellmarker", version="2.0", species="mouse")
    curated_df = cm.curate(df, reference_id=cm.name)

    curation = curated_df["__curated__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, True, True, False])

    assert curation.equals(expected_series)
