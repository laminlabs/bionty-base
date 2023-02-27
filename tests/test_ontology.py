import bionty as bt


def test_ontology_info():
    info = bt.dev.ontology_info("go")
    assert info["version"] == "2022-12-04"
    assert (
        info["versionIri"]
        == "http://purl.obolibrary.org/obo/go/releases/2022-12-04/go.owl"  # noqa: W503
    )
