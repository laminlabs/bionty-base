from pathlib import Path

import bionty as bt
from bionty._settings import settings
from bionty.dev._handle_sources import LAMINDB_INSTANCE_LOADED


def test_loaded_lamindb():
    import shutil

    shutil.copyfile(
        settings.current_sources.as_posix(), settings.lamindb_sources.as_posix()
    )

    lnenv = Path.home() / ".lamin/current_instance.env"
    with open(lnenv.as_posix(), "w") as f:
        f.write("schema_str=bionty")

    assert LAMINDB_INSTANCE_LOADED()

    ct = bt.CellType(version="2022-08-16")
    assert ct.source == "cl"

    lnenv.unlink()
    assert not LAMINDB_INSTANCE_LOADED()
