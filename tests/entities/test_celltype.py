import pandas as pd

import bionty as bt


def test_cl_celltype_curation_ontology_id():
    df = pd.DataFrame(
        index=[
            "CL:0002084",
            "CL:0002092",
            "CL:0002094",
            "CL:0002079",
            "This cell type does not exist",
        ]
    )

    ct = bt.CellType(source="cl", version="2022-08-16")
    curated_df = ct.curate(df)

    curation = curated_df["__curated__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, True, True, False])

    assert curation.equals(expected_series)


def test_cl_celltype_curation_name():
    df = pd.DataFrame(
        index=[
            "Boettcher cell",
            "bone marrow cell",
            "interstitial cell of ovary",
            "pancreatic ductal cell",
            "This cell type does not exist",
        ]
    )

    ct = bt.CellType(source="cl", version="2022-08-16")
    curated_df = ct.curate(df, reference_id=ct.name)

    curation = curated_df["__curated__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, True, True, False])

    assert curation.equals(expected_series)
