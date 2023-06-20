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

    pt = bt.Phenotype(source="hp", version="2023-06-17")
    inspected_df = pt.inspect(df.index, field=pt.name, return_df=True)

    inspect = inspected_df["__mapped__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, True, True, False])

    assert inspect.equals(expected_series)


def test_mp_phenotype_inspect_name():
    df = pd.DataFrame(
        index=[
            "decreased ovary apoptosis",
            "abnormal Ebner's gland morphology",
            "abnormal lacrimal sac morphology",
            "abnormal nictitating membrane morphology",
            "This phenotype does not exist",
        ]
    )

    pt = bt.Phenotype(source="mp", version="2023-05-31")
    inspected_df = pt.inspect(df.index, field=pt.name, return_df=True)

    inspect = inspected_df["__mapped__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, True, True, False])

    assert inspect.equals(expected_series)


def test_zp_phenotype_inspect_name():
    df = pd.DataFrame(
        index=[
            "somitogenesis disrupted, abnormal",
            "somite specification disrupted, abnormal",
            "liver has extra parts of type collagen trimer liver, abnormal",
            "neuromast hair cell normal process quality apoptotic process, abnormal",
            "This phenotype does not exist",
        ]
    )

    pt = bt.Phenotype(source="zp", version="2022-12-17")
    inspected_df = pt.inspect(df.index, field=pt.name, return_df=True)

    inspect = inspected_df["__mapped__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, True, True, False])

    assert inspect.equals(expected_series)
