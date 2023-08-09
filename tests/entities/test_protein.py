import pandas as pd

import bionty as bt


def test_uniprot_protein_inspect_uniprotkb_id():
    df = pd.DataFrame(
        index=[
            "A0A024QZ08",
            "X6RLV5",
            "X6RM24",
            "A0A024QZQ1",
            "This protein does not exist",
        ]
    )

    pr = bt.Protein(source="uniprot")
    inspected_df = pr.inspect(df.index, pr.uniprotkb_id, return_df=True)

    inspect = inspected_df["__validated__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, True, True, False])

    assert inspect.equals(expected_series)
