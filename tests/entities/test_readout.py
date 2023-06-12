import pandas as pd

import bionty as bt


def test_efo_readout_inspect_ontology_id():
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
    inspected_df = ro.inspect(df.index, ro.ontology_id, return_df=True)

    inspect = inspected_df["__mapped__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, True, True, False])

    assert inspect.equals(expected_series)


def test_readout_parse():
    ro = bt.Readout(source="efo", version="3.48.0")

    assert ro._parse("EFO:0008913") == {
        "ontology_id": "EFO:0008913",
        "name": "single-cell RNA sequencing",
        "molecule": "RNA assay",
        "instrument": "single cell sequencing",
        "measurement": None,
    }
