import pandas as pd

import bionty as bt


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

    pw = bt.Pathway(source="pw", version="7.74")
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

    pw = bt.Pathway(source="pw", version="7.74")
    curated_df = pw.curate(df, reference_id=pw.name)

    curation = curated_df["__curated__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, True, True, False])

    assert curation.equals(expected_series)
