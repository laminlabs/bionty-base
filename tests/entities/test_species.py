import pandas as pd

import bionty as bt


def test_ensemble_species_inspect_name():
    df = pd.DataFrame(
        index=[
            "spiny chromis",
            "silver-eye",
            "platyfish",
            "california sea lion",
            "This species does not exist",
        ]
    )

    sp = bt.Species(source="ensembl", version="release-109")
    inspected_df = sp.inspect(df.index, field=sp.name, return_df=True)

    inspect = inspected_df["__mapped__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, True, True, False])

    assert inspect.equals(expected_series)
