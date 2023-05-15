import pytest

import bionty as bt


@pytest.fixture(scope="session")
def cell_marker():
    cm_ids = [
        "KI67",
        "CCR7x",
        "CD14",
        "CD8",
        "CD45RA",
        "CD127",
        "PD1",
        "Invalid-1",
        "Invalid-2",
        "CD66b",
        "Siglec8",
        "Time",
    ]
    cm_entity = bt.CellMarker()

    return cm_ids, cm_entity


def test_inspect_iterable(cell_marker):
    cm_ids, cm_entity = cell_marker

    mapping = cm_entity.inspect(cm_ids, reference_id="name")

    print(mapping)


def test_inspect_return_df():
    pass
