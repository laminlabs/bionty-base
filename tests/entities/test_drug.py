import pandas as pd

import bionty as bt


def test_dron_drug_curation_ontology_id():
    df = pd.DataFrame(
        index=[
            "APOLLO:SV_00000145",
            "APOLLO:SV_00000336",
            "CHEBI:100147",
            "CHEBI:10023",
            "This drug does not exist",
        ]
    )
    dt = bt.Drug(source="dron", version="2023-03-10")
    curated_df = dt.curate(df)

    curation = curated_df["__curated__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, True, True, False])

    assert curation.equals(expected_series)


def test_dron_drug_curation_name():
    df = pd.DataFrame(
        index=[
            "resistance to infection",
            "resistance to malaria infection",
            "voriconazole",
            "nalidixic acid",
            "This disease does not exist",
        ]
    )

    dt = bt.Drug(source="dron", version="2023-03-10")
    curated_df = dt.curate(df, reference_id=dt.name)

    curation = curated_df["__curated__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, True, True, False])

    assert curation.equals(expected_series)
