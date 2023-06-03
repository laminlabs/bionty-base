import os
import tempfile
from unittest.mock import patch

import pytest
import yaml  # type:ignore

from bionty import update_defaults
from bionty.dev._handle_versions import MissingDefault


@pytest.fixture(scope="function")
def current_yaml_replica():
    input_file_content = """
    Species:
      all:
        ensembl: release-108
    Gene:
      human:
        ensembl: release-108
      mouse:
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
            MissingDefault(
                entity="Species",
                source="new database",
                species=["new species"],
                latest_version="new version",
            )
        ]

        update_defaults(new_defaults, "current")

        with open(current_yaml_replica, "r") as f:
            content = yaml.safe_load(f.read())

            assert "all" in content["Species"]
            assert "new database" in content["Species"]["new species"]
            assert "new version" in content["Species"]["new species"]["new database"]
