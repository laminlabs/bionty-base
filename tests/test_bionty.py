import pytest

import bionty as bt
from bionty.dev._handle_sources import CURRENT_SOURCES, LAMINDB_SOURCES, LOCAL_SOURCES


def test_unavailable_sources():
    with pytest.raises(ValueError):
        bt.CellType(source="random")


def test_reset_sources(monkeypatch):
    import shutil

    monkeypatch.setattr("builtins.input", lambda _: "y")

    shutil.copyfile(CURRENT_SOURCES.as_posix(), LAMINDB_SOURCES.as_posix())
    bt.reset_sources()

    CURRENT_SOURCES.unlink()
    LOCAL_SOURCES.unlink()
    bt.reset_sources()


def test_diff_successful():
    disease_bt_1 = bt.Disease(source="mondo", version="2023-04-04")
    disease_bt_2 = bt.Disease(source="mondo", version="2023-02-06")

    new_entries, modified_entries = disease_bt_1.diff(disease_bt_2)
    assert len(new_entries) == 819
    assert len(modified_entries) == 249


def test_diff_value_errors():
    # Two different Bionty object types
    disease_bt = bt.Disease()
    phenotype_bt = bt.Phenotype()
    with pytest.raises(ValueError):
        disease_bt.diff(phenotype_bt)

    # Different sources
    disease_bt_1 = bt.Disease(source="mondo")
    disease_bt_2 = bt.Disease(source="doid")
    with pytest.raises(ValueError):
        disease_bt_1.diff(disease_bt_2)

    # Same version
    disease_bt_3 = bt.Disease(source="mondo", version="2023-04-04")
    disease_bt_4 = bt.Disease(source="mondo", version="2023-04-04")
    with pytest.raises(ValueError):
        disease_bt_3.diff(disease_bt_4)
