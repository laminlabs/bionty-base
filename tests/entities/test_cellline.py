import pandas as pd

import bionty as bt


def test_clo_cellline_curation_ontology_id():
    df = pd.DataFrame(
        index=[
            "CLO:0001210",
            "CLO:0001230",
            "CLO:0001248",
            "CLO:0001225",
            "This cell line does not exist",
        ]
    )

    cl = bt.CellLine(source="clo", version="2022-03-21")
    curated_df = cl.curate(df)

    curation = curated_df["__curated__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, True, True, False])

    assert curation.equals(expected_series)


def test_clo_cellline_curation_name():
    df = pd.DataFrame(
        index=[
            "253D cell",
            "HEK293",
            "2C1H7 cell",
            "283TAg cell",
            "This cell line does not exist",
        ]
    )

    cl = bt.CellLine(source="clo", version="2022-03-21")
    curated_df = cl.curate(df, reference_id=cl.name)

    curation = curated_df["__curated__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, True, True, False])

    assert curation.equals(expected_series)
