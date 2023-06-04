import os
import tempfile

import pytest

# from unittest.mock import patch


@pytest.fixture(scope="function")
def versions_yaml_replica():
    input_file_content = """
    version: "0.2.0"
    Species:
      ensembl:
        versions:
          release-108:
            source: https://ftp.ensembl.org/pub/release-108/mysql/
            md5: ""
        species:
          - all
        name: Ensembl
        website: https://www.ensembl.org/index.html
    Gene:
      ensembl:
        versions:
          release-108:
            source: https://ftp.ensembl.org/pub/release-108/mysql/
            md5: ""
          release-107:
            source: https://ftp.ensembl.org/pub/release-107/mysql/
            md5: ""
        species:
          - human
          - mouse
        name: Ensembl
        website: https://www.ensembl.org/index.html
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
      all:
        ensembl: release-108
    """
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as f:
        f.write(input_file_content)
        f.flush()
        yield f.name

    os.unlink(f.name)


# def test_get_missing_defaults(versions_yaml_replica, current_yaml_replica):
#     with patch.multiple(
#         "bionty.dev._handle_versions",
#         VERSIONS_PATH=versions_yaml_replica,
#         _CURRENT_PATH=current_yaml_replica,
#     ):
#         expected = [
#             (
#                 "Gene",
#                 "ensembl",
#                 "human",
#                 "release-108",
#             ),
#             (
#                 "Gene",
#                 "ensembl",
#                 "mouse",
#                 "release-108",
#             ),
#         ]
#         from bionty.dev._handle_versions import _get_missing_defaults

#         result = _get_missing_defaults(source="versions")
#         assert result == expected
