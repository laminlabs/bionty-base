from bionty.dev import current_db_version


def test_current_db_version():
    v = current_db_version(db="ensembl")
    assert v.startswith("release-")
