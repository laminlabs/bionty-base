import bionty as bt
from bionty.dev._io import s3_bionty_assets


def test_ontology():
    localpath = s3_bionty_assets("ontology_all__pw__7.79__Pathway")
    onto = bt.Ontology(localpath)
    assert onto.get_term("PW:0000014").name == "neurodegenerative pathway"
    df = onto.to_df(source="pw", include_id_prefixes={"pw": ["PW"]})
    assert df.shape == (2613, 4)
    assert df.index.name == "ontology_id"
