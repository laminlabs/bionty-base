import pandas as pd

import bionty as bt


def test_ensemble_species_curation_ontology_id():
    df = pd.DataFrame(
        index=[
            "NCBI_80966",
            "NCBI_211598",
            "NCBI_241587",
            "NCBI_44394",
            "This species does not exist",
        ]
    )
    curated_df = bt.Species(database="ensembl", version="release-108").curate(
        df, reference_index="id"
    )

    curation = curated_df["__curated__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, True, True, False])

    assert curation.equals(expected_series)


def test_ensemble_species_curation_name():
    df = pd.DataFrame(
        index=[
            "spiny chromis",
            "silver-eye",
            "platyfish",
            "california sea lion",
            "This species does not exist",
        ]
    )
    curated_df = bt.Species(database="ensembl", version="release-108").curate(
        df, reference_index="name"
    )

    curation = curated_df["__curated__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, True, True, False])

    assert curation.equals(expected_series)
