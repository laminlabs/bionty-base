from pathlib import Path

import bionty as bt
from bionty.dev._handle_sources import (
    CURRENT_SOURCES,
    LAMINDB_INSTANCE_LOADED,
    LAMINDB_SOURCES,
)


def test_loaded_lamindb():
    import shutil

    shutil.copyfile(CURRENT_SOURCES.as_posix(), LAMINDB_SOURCES.as_posix())

    lnenv = Path.home() / ".lamin/current_instance.env"
    with open(lnenv.as_posix(), "w") as f:
        f.write("schema_str=bionty")

    assert LAMINDB_INSTANCE_LOADED()

    ct = bt.CellType(version="2022-08-16")
    assert ct.source == "cl"

    lnenv.unlink()
    assert not LAMINDB_INSTANCE_LOADED()
