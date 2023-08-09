import os
from pathlib import Path
from typing import Tuple

import pytest

from bionty.dev._md5 import calculate_md5, verify_md5

CURRENT_DIR = Path(__file__).parent


@pytest.fixture(scope="module")
def file_fixture() -> Tuple[str, str]:  # type: ignore
    file_path = "test_file.txt"
    with open(file_path, "w") as f:
        f.write("Hello, world!")
    expected_md5 = calculate_md5(file_path)
    yield file_path, expected_md5
    os.remove(file_path)


def test_verify_md5_with_matching_md5(file_fixture):
    file_path, expected_md5 = file_fixture
    assert verify_md5(file_path, expected_md5)


def test_verify_md5_with_non_matching_md5(file_fixture):
    file_path, _ = file_fixture
    assert not verify_md5(file_path, "0123456789abcdef0123456789abcdef")
