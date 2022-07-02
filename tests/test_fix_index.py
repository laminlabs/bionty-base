import pandas as pd
import pytest

from bionty.dev import get_compliant_index_from_column

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


def test_get_compliant_index_from_column():
    with pytest.raises(AssertionError):
        get_compliant_index_from_column(df, df, column="bla")
