from bionty.dev._handle_versions import latest_db_version


def test_current_db_version():
    v = latest_db_version(db="ensembl")
    assert v.startswith("release-")
