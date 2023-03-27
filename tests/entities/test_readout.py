import pandas as pd

import bionty as bt


def test_efo_readout_curation_ontology_id():
    df = pd.DataFrame(
        index=[
            "EFO:0000001",
            "EFO:1002050",
            "EFO:1002047",
            "EFO:0000005",
            "This readout does not exist",
        ]
    )
    curated_df = bt.Readout(database="efo", version="3.48.0").curate(df)

    curation = curated_df["__curated__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, True, True, False])

    assert curation.equals(expected_series)


def test_efo_readout_curation_name():
    df = pd.DataFrame(
        index=[
            "CS57511",
            "CS57520",
            "CS57515",
            "experimental factor",
            "This readout does not exist",
        ]
    )
    curated_df = bt.Readout(database="efo", version="3.48.0").curate(
        df, reference_id="name"
    )

    curation = curated_df["__curated__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, True, True, False])

    assert curation.equals(expected_series)
