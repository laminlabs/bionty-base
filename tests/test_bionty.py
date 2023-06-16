from pathlib import Path

import pytest

import bionty as bt
from bionty.dev._handle_sources import CURRENT_SOURCES, LAMINDB_SOURCES


def test_unavailable_sources():
    with pytest.raises(ValueError):
        bt.CellType(source="random")


@pytest.fixture(scope="module")
def test_loaded_lamindb():
    lnenv = Path.home() / ".lamin/current_instance.env"
    open(lnenv, "a").close()
    ct = bt.CellType(version="2022-08-16")
    assert ct.source is None
    assert str(ct) == "invalid Bionty object"
    import shutil

    shutil.copyfile(CURRENT_SOURCES, LAMINDB_SOURCES)
