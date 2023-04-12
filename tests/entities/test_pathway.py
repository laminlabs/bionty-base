import pandas as pd

import bionty as bt


def test_pw_pathway_curation_ontology_id():
    df = pd.DataFrame(
        index=[
            "Reactome:R-HSA-73780",
            "KEGG:00730",
            "GO:0006385",
            "OMIM:236130",
            "This pathway does not exist",
        ]
    )
    curated_df = bt.Pathway(database="pw", version="7.74").curate(df)

    curation = curated_df["__curated__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, True, True, False])

    assert curation.equals(expected_series)
