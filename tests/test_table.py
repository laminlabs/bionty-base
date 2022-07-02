import pandas as pd

from bionty import Gene

data = {
    "hgnc_symbol": ["A1CF", "A1BG", "corrupted1", "corrupted2"],
    "hgnc_id": ["HGNC:24086", "HGNC:5", "corrupted1", "corrupted2"],
    "ensembl.gene_id": [
        "ENSG00000148584",
        "ENSG00000121410",
        "corrupted1",
        "corrupted2",
    ],
}
df = pd.DataFrame(data).set_index("hgnc_id")


def test_curate():
    df_curated = Gene().curate(df.set_index("hgnc_symbol"))
    assert df_curated.index.to_list() == ["A1CF", "A1BG", "corrupted1", "corrupted2"]
    assert df_curated.__curated__.to_list() == [True, True, False, False]
