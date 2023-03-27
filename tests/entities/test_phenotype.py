import pandas as pd

import bionty as bt


def test_hp_phenotype_curation_ontology_id():
    df = pd.DataFrame(
        index=[
            "BFO:0000001",
            "HGNC:9958",
            "HGNC:8582",
            "BFO:0000006",
            "This phenotype does not exist",
        ]
    )
    curated_df = bt.Phenotype(database="hp", version="2023-01-27").curate(df)

    curation = curated_df["__curated__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, True, True, False])

    assert curation.equals(expected_series)


def test_hp_phenotype_curation_name():
    df = pd.DataFrame(
        index=[
            "eukaryotic protein",
            "Fixated interest with abnormal intensity",
            "Hand-leading gestures",
            "Idiosyncratic language",
            "This phenotype does not exist",
        ]
    )
    curated_df = bt.Phenotype(database="hp", version="2023-01-27").curate(
        df, reference_id="name"
    )

    curation = curated_df["__curated__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, True, True, False])

    assert curation.equals(expected_series)
