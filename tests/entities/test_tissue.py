import pandas as pd

import bionty as bt


def test_uberon_tissue_curation_ontology_id():
    df = pd.DataFrame(
        index=[
            "UBERON:0000000",
            "UBERON:0000005",
            "UBERON:8600001",
            "UBERON:8600002",
            "This cell line does not exist",
        ]
    )
    curated_df = bt.Tissue().curate(df)

    curation = curated_df["__curated__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, True, True, False])

    assert curation.equals(expected_series)


# def test_uberon_tissue_curation_name():
#     df = pd.DataFrame(
#         index=[
#             "DA05702 cell",
#             "DA05703 cell",
#             "immortal astrocyte cell line cell",
#             "15P-1 cell",
#             "This cell line does not exist",
#         ]
#     )
#     curated_df = bt.Tissue(id="name").curate(df)
#
#     curation = curated_df["__curated__"].reset_index(drop=True)
#     expected_series = pd.Series([True, True, True, True, False])
#
#     assert curation.equals(expected_series)
