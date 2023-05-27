import pandas as pd

import bionty as bt


def test_dron_drug_curation_ontology_id():
    df = pd.DataFrame(
        index=[
            "DRON:00018440",
            "DRON:00018432",
            "DRON:00018438",
            "DRON:00018452",
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
            "LILIUM LONGIFLORIUM",
            "citrus bioflavonoids",
            "Ornithine, (L)-Isomer",
            "Hyoscyamus extract",
            "This disease does not exist",
        ]
    )

    dt = bt.Drug(source="dron", version="2023-03-10")
    curated_df = dt.curate(df, reference_id=dt.name)

    curation = curated_df["__curated__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, True, True, False])

    assert curation.equals(expected_series)
