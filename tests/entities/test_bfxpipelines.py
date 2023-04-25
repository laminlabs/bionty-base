import pandas as pd

import bionty as bt


def test_lamin_bfxpipeline_curation_ontology_id():
    df = pd.DataFrame(
        index=[
            "xtRZ4Laj9",
            "X3VHWbArB",
            "This bfx pipeline does not exist",
        ]
    )

    curated_df = bt.BFXPipelines(database="lamin", version="1.0.0").curate(df)

    curation = curated_df["__curated__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, False])

    assert curation.equals(expected_series)


def test_lamin_bfxpipeline_curation_name():
    df = pd.DataFrame(
        index=[
            "methylseq v2.3.0",
            "Cell Ranger v7.1.0",
            "This bfx pipeline does not exist",
        ]
    )

    curated_df = bt.BFXPipelines(database="lamin", version="1.0.0").curate(
        df, reference_id="name"
    )

    curation = curated_df["__curated__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, False])

    assert curation.equals(expected_series)
