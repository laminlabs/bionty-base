import pandas as pd

import bionty as bt


def test_mondo_disease_inspect_name():
    df = pd.DataFrame(
        index=[
            "supraglottis cancer",
            "alexia",
            "trigonitis",
            "paranasal sinus disorder",
            "This disease does not exist",
        ]
    )

    ds = bt.Disease(source="mondo", version="2023-04-04")
    inspected_df = ds.inspect(df.index, field=ds.name, return_df=True)

    inspect = inspected_df["__mapped__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, True, True, False])

    assert inspect.equals(expected_series)


def test_doid_disease_inspect_ontology_id():
    df = pd.DataFrame(
        index=[
            "DOID:0001816",
            "DOID:0002116",
            "DOID:5547",
            "DOID:5551",
            "This disease does not exist",
        ]
    )

    ds = bt.Disease(source="doid", version="2023-03-31")
    inspected_df = ds.inspect(df.index, field=ds.ontology_id, return_df=True)

    inspect = inspected_df["__mapped__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, True, True, False])

    assert inspect.equals(expected_series)
