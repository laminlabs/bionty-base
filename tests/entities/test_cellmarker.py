import pandas as pd

import bionty as bt


def test_uniprot_cellmarker_curation_ontology_id():
    df = pd.DataFrame(
        index=["CCR7", "CD69", "CD8A", "CD45RA", "This protein does not exist"]
    )

    curated_df = bt.CellMarker(database="cellmarker", version="2.0").curate(df)

    curation = curated_df["__curated__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, True, True, False])

    assert curation.equals(expected_series)


def test_uniprot_cellmarker_curation_name():
    df = pd.DataFrame(
        index=[
            "1-MAR",
            "160 KDA NEUROFILAMENT MEDIUM",
            "VON WILLEBRAND FACTOR",
            "TYPE IV COLLAGEN",
            "This protein does not exist",
        ]
    )
    curated_df = bt.CellMarker(id="name", database="cellmarker", version="2.0").curate(
        df
    )

    curation = curated_df["__curated__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, True, True, False])

    assert curation.equals(expected_series)
