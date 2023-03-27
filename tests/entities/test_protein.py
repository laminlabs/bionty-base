import pandas as pd

import bionty as bt


def test_uniprot_protein_curation_uniprotkb_id():
    df = pd.DataFrame(
        index=[
            "A0A024QZ08",
            "X6RLV5",
            "X6RM24",
            "A0A024QZQ1",
            "This cell line does not exist",
        ]
    )
    curated_df = bt.Protein(database="uniprot", version="2022-04").curate(df)

    curation = curated_df["__curated__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, True, True, False])

    assert curation.equals(expected_series)


def test_uniprot_protein_curation_name():
    df = pd.DataFrame(
        index=[
            "isoform CRA_c",
            "Battenin",
            "Probable ATP-dependent RNA helicase DDX5",
            "isoform CRA_a",
            "This cell line does not exist",
        ]
    )
    curated_df = bt.Protein(database="uniprot", version="2022-04").curate(
        df, reference_id="name"
    )

    curation = curated_df["__curated__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, True, True, False])

    assert curation.equals(expected_series)
