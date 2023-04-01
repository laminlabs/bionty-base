import os
import tempfile
from unittest.mock import patch

import pytest


@pytest.fixture(scope="function")
def versions_yaml_replica():
    input_file_content = """
    version: "0.1.0"
    Species:
      ensembl:
        versions:
          release-108:
            - https://ftp.ensembl.org/pub/release-108/mysql/
            - ""
        name: Ensembl
        website: https://www.ensembl.org/index.html
    Gene:
      ensembl:
        versions:
          release-108:
            - https://ftp.ensembl.org/pub/release-108/mysql/
            - ""
          release-107:
            - https://ftp.ensembl.org/pub/release-107/mysql/
            - ""
        name: Ensembl
        website: https://www.ensembl.org/index.html
    Pathway:
      pw:
        versions:
          7.74:
            - https://data.bioontology.org/ontologies/PW/filename
            - a6df86616149dcdfe08fe16c900cba85
          99.99:
            - https://data.bioontology.org/ontologies/PW/filename
            - a6df86616149dcdfe08fe16c900cba85
        name: Pathway Ontology
        website: https://www.ebi.ac.uk/ols/ontologies/pw
    """
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as f:
        f.write(input_file_content)
        f.flush()
        yield f.name

    os.unlink(f.name)


@pytest.fixture(scope="function")
def current_yaml_replica():
    input_file_content = """
    Species:
        ensembl: release-108
    Gene:
        ensembl: release-108
    """
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as f:
        f.write(input_file_content)
        f.flush()
        yield f.name

    os.unlink(f.name)


def test_get_missing_defaults(versions_yaml_replica, current_yaml_replica):
    with patch.multiple(
        "bionty.dev._handle_versions",
        VERSIONS_PATH=versions_yaml_replica,
        _CURRENT_PATH=current_yaml_replica,
    ):
        expected = [("Pathway", "pw", "7.74")]
        from bionty.dev._handle_versions import _get_missing_defaults

        result = _get_missing_defaults(source="versions")
        assert result == expected
