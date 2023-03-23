import pandas as pd

import bionty as bt


def test_uberon_tissue_curation_ontology_id():
    df = pd.DataFrame(
        index=[
            "UBERON:0000000",
            "UBERON:0000005",
            "UBERON:8600001",
            "UBERON:8600002",
            "This tissue does not exist",
        ]
    )
    curated_df = bt.Tissue(database="uberon", version="2023-02-14").curate(df)

    curation = curated_df["__curated__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, True, True, False])

    assert curation.equals(expected_series)


def test_uberon_tissue_curation_name():
    df = pd.DataFrame(
        index=[
            "nose",
            "chemosensory organ",
            "epithelium of lobular bronchiole",
            "smooth muscle tissue of lobular bronchiole",
            "This tissue does not exist",
        ]
    )
    curated_df = bt.Tissue(database="uberon", version="2023-02-14").curate(
        df, reference_index="name"
    )

    curation = curated_df["__curated__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, True, True, False])

    assert curation.equals(expected_series)
