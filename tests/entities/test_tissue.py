import pandas as pd

import bionty as bt


def test_uberon_tissue_curation_ontology_id():
    df = pd.DataFrame(
        index=[
            "http://birdgenenames.org/cgnc/GeneReport?id=49160",
            "http://www.ncbi.nlm.nih.gov/gene/396453",
            "http://www.ncbi.nlm.nih.gov/gene/396217",
            "http://birdgenenames.org/cgnc/GeneReport?id=16227",
            "This cell line does not exist",
        ]
    )
    curated_df = bt.Tissue().curate(df)

    curation = curated_df["__curated__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, True, True, False])

    assert curation.equals(expected_series)


# TODO Something is also off here. All names are None.
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
