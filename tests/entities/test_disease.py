import pandas as pd

import bionty as bt


def test_mondo_disease_curation_ontology_id():
    df = pd.DataFrame(
        index=[
            "MONDO:0001724",
            "MONDO:0001712",
            "MONDO:0001732",
            "MONDO:0001735",
            "This disease does not exist",
        ]
    )

    ds = bt.Disease(source="mondo", version="2023-02-06")
    curated_df = ds.curate(df)

    curation = curated_df["__curated__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, True, True, False])

    assert curation.equals(expected_series)


def test_mondo_disease_curation_name():
    df = pd.DataFrame(
        index=[
            "supraglottis cancer",
            "alexia",
            "trigonitis",
            "paranasal sinus disorder",
            "This disease does not exist",
        ]
    )

    ds = bt.Disease(source="mondo", version="2023-02-06")
    curated_df = ds.curate(df, reference_id=ds.name)

    curation = curated_df["__curated__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, True, True, False])

    assert curation.equals(expected_series)


def test_doid_disease_curation_ontology_id():
    df = pd.DataFrame(
        index=[
            "DOID:0001816",
            "DOID:0002116",
            "DOID:5547",
            "DOID:5551",
            "This disease does not exist",
        ]
    )

    ds = bt.Disease(source="doid", version="2023-01-30")
    curated_df = ds.curate(df)

    curation = curated_df["__curated__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, True, True, False])

    assert curation.equals(expected_series)


def test_doid_disease_curation_name():
    df = pd.DataFrame(
        index=[
            "aspirin allergy",
            "foramen magnum meningioma",
            "skull base meningioma",
            "choriocarcinoma of the testis",
            "This disease does not exist",
        ]
    )

    ds = bt.Disease(source="doid", version="2023-01-30")
    curated_df = ds.curate(df, reference_id=ds.name)

    curation = curated_df["__curated__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, True, True, False])

    assert curation.equals(expected_series)
