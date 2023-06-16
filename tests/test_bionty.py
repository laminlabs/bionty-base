import pytest

import bionty as bt
from bionty.dev._handle_sources import CURRENT_SOURCES, LAMINDB_SOURCES, LOCAL_SOURCES


def test_unavailable_sources():
    with pytest.raises(ValueError):
        bt.CellType(source="random")


def test_reset_sources():
    import shutil

    shutil.copyfile(CURRENT_SOURCES.as_posix(), LAMINDB_SOURCES.as_posix())
    bt.reset_sources()
    bt.reset_sources(confirm=True)

    CURRENT_SOURCES.unlink()
    LOCAL_SOURCES.unlink()
    bt.reset_sources(confirm=True)
