import pandas as pd

import bionty as bt


def test_lamin_bfxpipeline_inspect_name():
    df = pd.DataFrame(
        index=[
            "methylseq v2.3.0",
            "Cell Ranger v7.1.0",
            "This bfx pipeline does not exist",
        ]
    )

    bfxp = bt.BFXPipeline(source="lamin", version="1.0.0")
    inspected_df = bfxp.inspect(df.index, field=bfxp.name, return_df=True)

    inspect = inspected_df["__mapped__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, False])

    assert inspect.equals(expected_series)
