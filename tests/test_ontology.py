import bionty as bt
from bionty._ontology import Ontology
from bionty.dev._io import s3_bionty_assets


def test_ontology_info():
    info = bt.dev.ontology_info("go")
    assert info["version"] == "2022-12-04"
    assert (
        info["versionIri"]
        == "http://purl.obolibrary.org/obo/go/releases/2022-12-04/go.owl"  # noqa: W503
    )


def test_ontology():
    localpath = s3_bionty_assets("all___pw___7.79___Pathway")
    onto = Ontology(localpath)
    onto.get_term("PW:0000014").name == "neurodegenerative pathway"
    df = onto.to_df(source="pw", include_id_prefixes={"pw": ["PW"]})
    df.shape == (2613, 4)
    df.index.name == "ontology_id"
