import pandas as pd

import bionty as bt


def test_hp_phenotype_curation_ontology_id():
    df = pd.DataFrame(
        index=[
            "HP:0001328",
            "HP:0001332",
            "HP:0001342",
            "HP:0001350",
            "This phenotype does not exist",
        ]
    )

    pt = bt.Phenotype(source="hp", version="2023-01-27")
    curated_df = pt.curate(df)

    curation = curated_df["__curated__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, True, True, False])

    assert curation.equals(expected_series)


def test_hp_phenotype_curation_name():
    df = pd.DataFrame(
        index=[
            "Specific learning disability",
            "Dystonia",
            "Cerebral hemorrhage",
            "Slurred speech",
            "This phenotype does not exist",
        ]
    )

    pt = bt.Phenotype(source="hp", version="2023-01-27")
    curated_df = pt.curate(df, reference_id=pt.name)

    curation = curated_df["__curated__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, True, True, False])

    assert curation.equals(expected_series)
