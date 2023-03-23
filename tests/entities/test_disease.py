import pandas as pd

import bionty as bt


def test_mondo_disease_curation_ontology_id():
    df = pd.DataFrame(
        index=[
            "UBERON:8440004",
            "UPHENO:0001001",
            "UBERON:8420000",
            "http://identifiers.org/hgnc/10001",
            "This disease does not exist",
        ]
    )
    curated_df = bt.Disease(database="mondo", version="2023-02-06").curate(df)

    curation = curated_df["__curated__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, True, True, False])

    assert curation.equals(expected_series)


def test_mondo_disease_curation_name():
    df = pd.DataFrame(
        index=[
            "laminar subdivision of the cortex",
            "hair of scalp",
            "RHAG",
            "GRK1",
            "This disease does not exist",
        ]
    )
    curated_df = bt.Disease(database="mondo", version="2023-02-06").curate(
        df, reference_index="name"
    )

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
    curated_df = bt.Disease(database="doid", version="2023-01-30").curate(df)

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
    curated_df = bt.Disease(database="doid", version="2023-01-30").curate(
        df, reference_index="name"
    )

    curation = curated_df["__curated__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, True, True, False])

    assert curation.equals(expected_series)
