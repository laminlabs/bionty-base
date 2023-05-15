import pandas as pd

import bionty as bt


def test_cl_celltype_curation_ontology_id():
    df = pd.DataFrame(
        index=[
            "BFO:0000002",
            "BFO:0000004",
            "UBERON:8480008",
            "UBERON:8480004",
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
            "placental artery",
            "placental artery endothelium",
            "spatial region",
            "continuant",
            "This cell type does not exist",
        ]
    )

    ct = bt.CellType(source="cl", version="2022-08-16")
    curated_df = ct.curate(df, reference_id=ct.name)

    curation = curated_df["__curated__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, True, True, False])

    assert curation.equals(expected_series)


def test_ca_celltype_curation_ontology_id():
    df = pd.DataFrame(
        index=[
            "CL:0000084",
            "CL:0000542",
            "CL:0000052",
            "CL:0000320",
            "This cell type does not exist",
        ]
    )

    curated_df = bt.CellType(source="ca", version="2022-12-16").curate(df)

    curation = curated_df["__curated__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, True, True, False])

    assert curation.equals(expected_series)


def test_ca_celltype_curation_name():
    df = pd.DataFrame(
        index=[
            "placental epithelial cell",
            "response to estradiol",
            "capillary",
            "serosa of esophagus",
            "This cell type does not exist",
        ]
    )
    curated_df = bt.CellType(source="ca", version="2022-12-16").curate(
        df, reference_id="name"
    )

    curation = curated_df["__curated__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, True, True, False])

    assert curation.equals(expected_series)
