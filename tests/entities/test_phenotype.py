import pandas as pd

import bionty as bt


def test_hp_phenotype_inspect_name():
    df = pd.DataFrame(
        index=[
            "Specific learning disability",
            "Dystonia",
            "Cerebral hemorrhage",
            "Slurred speech",
            "This phenotype does not exist",
        ]
    )

    pt = bt.Phenotype(source="hp", version="2023-01-27")
    inspected_df = pt.inspect(df.index, field=pt.name, return_df=True)

    inspect = inspected_df["__mapped__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, True, True, False])

    assert inspect.equals(expected_series)
