import os
import tempfile
from unittest.mock import patch

import pytest

from bionty import update_defaults


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
    """
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as f:
        f.write(input_file_content)
        f.flush()
        yield f.name

    os.unlink(f.name)


def test_update_defaults(versions_yaml_replica):
    # Patch _CURRENT_PATH to point to a temporary file
    with patch("bionty._sync_versions._CURRENT_PATH", versions_yaml_replica):
        new_defaults = [
            ("Species", "new_database", "new_version"),
            ("Gene", "new_database", "new_version"),
        ]

        update_defaults(new_defaults, "current")

        with open(versions_yaml_replica, "r") as f:
            content = f.read()
            assert (
                "new_database: new_version"
                in content.split("Species:\n", 1)[1].split("\nGene:", 1)[0]
            )
