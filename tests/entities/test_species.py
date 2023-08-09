import pandas as pd

import bionty as bt


def test_ensembl_species_inspect_name():
    df = pd.DataFrame(
        index=[
            "spiny chromis",
            "silver-eye",
            "platyfish",
            "california sea lion",
            "This species does not exist",
        ]
    )

    sp = bt.Species(source="ensembl")
    inspected_df = sp.inspect(df.index, field=sp.name, return_df=True)

    inspect = inspected_df["__validated__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, True, True, False])

    assert inspect.equals(expected_series)


def test_ensembl_species_species():
    for sp in ["bacteria", "plants", "fungi", "metazoa"]:
        df = bt.Species(species=sp).df()
        assert df.shape[0] > 10
