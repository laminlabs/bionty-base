import pandas as pd

from bionty._lookup import Lookup


def test_lookup():
    df = pd.DataFrame(
        {
            "name": ["Sample 1", "Sample 1", "sample 1", "1 sample"],
            "meta1": ["metadata~1", "metadata~1~1", "metadata~1~1~1", "1 metadata"],
        }
    )

    inst = Lookup(df=df, field="name", tuple_name="TestTuple", prefix="prefix")
    lookup = inst.lookup()

    assert len(lookup.sample_1) == 3
    assert isinstance(lookup.sample_1, list)
    assert lookup.sample_1[0]._asdict() == {"name": "Sample 1", "meta1": "metadata~1~1"}
    assert lookup.sample_1[1]._asdict() == {"name": "Sample 1", "meta1": "metadata~1"}
    assert lookup.sample_1[2]._asdict() == {
        "name": "sample 1",
        "meta1": "metadata~1~1~1",
    }
    assert lookup.prefix_1_sample._asdict() == {
        "name": "1 sample",
        "meta1": "1 metadata",
    }

    lookup_dict = lookup.todict()
    assert len(lookup_dict) == 3
    assert isinstance(lookup_dict["Sample 1"], list)
    assert len(lookup_dict["Sample 1"]) == 2
    assert isinstance(lookup_dict["sample 1"], tuple)
    assert lookup_dict["1 sample"]._asdict() == {
        "name": "1 sample",
        "meta1": "1 metadata",
    }

    assert lookup.__class__.__name__ == "Lookup"
    assert lookup.prefix_1_sample.__class__.__name__ == "TestTuple"
