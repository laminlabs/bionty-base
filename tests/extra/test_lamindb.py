from pathlib import Path

import bionty as bt
from bionty.dev._handle_sources import CURRENT_SOURCES, LAMINDB_SOURCES


def test_loaded_lamindb():
    import shutil

    shutil.copyfile(CURRENT_SOURCES, LAMINDB_SOURCES)

    lnenv = Path.home() / ".lamin/current_instance.env"
    open(lnenv, "a").close()

    ct = bt.CellType(version="2022-08-16")
    assert ct.source is None
    assert str(ct) == "invalid Bionty object"
