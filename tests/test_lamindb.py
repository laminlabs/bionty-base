from pathlib import Path

import bionty as bt
from bionty.dev._handle_sources import CURRENT_SOURCES, LAMINDB_SOURCES


def test_loaded_lamindb():
    import shutil

    shutil.copyfile(CURRENT_SOURCES.as_posix(), LAMINDB_SOURCES.as_posix())

    lnenv = Path.home() / ".lamin/current_instance.env"
    with open(lnenv.as_posix(), "w") as f:
        f.write("schema_str=bionty")

    ct = bt.CellType(version="2022-08-16")
    assert ct.source is None
    assert str(ct) == "invalid Bionty object"

    lnenv.unlink()
