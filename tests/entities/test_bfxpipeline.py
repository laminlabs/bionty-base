import bionty_base as bt
import pandas as pd


def test_lamin_bfxpipeline_inspect_name():
    df = pd.DataFrame(
        index=[
            "nf-core methylseq",
            "Cell Ranger",
            "This bfx pipeline does not exist",
        ]
    )

    bfxp = bt.BFXPipeline(source="lamin")
    inspected_df = bfxp.inspect(df.index, field=bfxp.name, return_df=True)

    inspect = inspected_df["__validated__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, False])

    assert inspect.equals(expected_series)
