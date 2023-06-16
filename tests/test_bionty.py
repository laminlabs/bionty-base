from pathlib import Path

import pytest

import bionty as bt


def test_unavailable_sources():
    with pytest.raises(ValueError):
        bt.CellType(source="random")


def test_loaded_lamindb():
    lnenv = Path.home() / ".lamin/current_instance.env"
    open(lnenv, "a").close()
    ct = bt.CellType(version="2022-08-16")
    assert ct.source is None
    assert str(ct) == "invalid Bionty object"
    lnenv.unlink()
