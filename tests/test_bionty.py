import pytest

import bionty as bt


def test_unavailable_sources():
    with pytest.raises(ValueError):
        bt.CellType(source="random")
