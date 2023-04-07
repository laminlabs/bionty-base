import os
import tempfile
from unittest.mock import patch

import pytest

from bionty import update_defaults


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


def test_update_defaults(current_yaml_replica):
    with patch("bionty._sync_versions._CURRENT_PATH", current_yaml_replica):
        new_defaults = [
            ("Species", "new_database", "new_version"),
            ("Gene", "new_database", "new_version"),
        ]

        update_defaults(new_defaults, "current")

        with open(current_yaml_replica, "r") as f:
            content = f.read()
            content_split = content.split("\n")
            species_content = content_split[1].strip()
            assert '"new_database": "new_version"' in species_content
