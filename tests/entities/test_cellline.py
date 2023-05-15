import pandas as pd

import bionty as bt


def test_clo_cellline_curation_ontology_id():
    df = pd.DataFrame(
        index=[
            "BFO:0000003",
            "http://www.ebi.ac.uk/efo/EFO_0002970",
            "http://www.ebi.ac.uk/efo/EFO_0002970",
            "BFO:0000004",
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
            "DA05702 cell",
            "DA05703 cell",
            "immortal astrocyte cell line cell",
            "15P-1 cell",
            "This cell line does not exist",
        ]
    )

    cl = bt.CellLine(source="clo", version="2022-03-21")
    curated_df = cl.curate(df, reference_id=cl.name)

    curation = curated_df["__curated__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, True, True, False])

    assert curation.equals(expected_series)
