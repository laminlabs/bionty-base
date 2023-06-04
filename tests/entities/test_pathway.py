import pandas as pd

import bionty as bt


def test_pw_go_curation_ontology_id():
    df = pd.DataFrame(
        index=[
            "GO:1905210",
            "GO:1905211",
            "GO:1905212",
            "GO:1905208",
            "This pathway does not exist",
        ]
    )

    pw = bt.Pathway(source="go", version="2023-05-10")
    curated_df = pw.curate(df)

    curation = curated_df["__curated__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, True, True, False])

    assert curation.equals(expected_series)


def test_pw_go_curation_name():
    df = pd.DataFrame(
        index=[
            "regulation of fibroblast chemotaxis",
            "negative regulation of fibroblast chemotaxis",
            "positive regulation of fibroblast chemotaxis",
            "negative regulation of cardiocyte differentiation",
            "This pathway does not exist",
        ]
    )

    pw = bt.Pathway(source="go", version="2023-05-10")
    curated_df = pw.curate(df, reference_id=pw.name)

    curation = curated_df["__curated__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, True, True, False])

    assert curation.equals(expected_series)


def test_pw_pathway_curation_ontology_id():
    df = pd.DataFrame(
        index=[
            "PW:0000049",
            "PW:0000009",
            "PW:0000001",
            "PW:0002000",
            "This pathway does not exist",
        ]
    )

    pw = bt.Pathway(source="pw", version="7.79")
    curated_df = pw.curate(df)

    curation = curated_df["__curated__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, True, True, False])

    assert curation.equals(expected_series)


def test_pw_pathway_curation_name():
    df = pd.DataFrame(
        index=[
            "Toll-like receptor 9 signaling pathway",
            "Toll-like receptor TLR1:TLR2 signaling pathway",
            "classic metabolic pathway",
            "regulatory pathway",
            "This pathway does not exist",
        ]
    )

    pw = bt.Pathway(source="pw", version="7.79")
    curated_df = pw.curate(df, reference_id=pw.name)

    curation = curated_df["__curated__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, True, True, False])

    assert curation.equals(expected_series)
