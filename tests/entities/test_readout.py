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

    ro = bt.Readout(source="efo", version="3.48.0")
    curated_df = ro.curate(df)

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

    ro = bt.Readout(source="efo", version="3.48.0")
    curated_df = ro.curate(df, reference_id=ro.name)

    curation = curated_df["__curated__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, True, True, False])

    assert curation.equals(expected_series)


def test_readout_parse():
    ro = bt.Readout(source="efo", version="3.48.0")

    assert ro._parse("EFO:0008913") == {
        "ontology_id": "EFO:0008913",
        "name": "single-cell RNA sequencing",
        "molecule": "RNA assay",
        "instrument": "single cell sequencing",
        "measurement": None,
    }
