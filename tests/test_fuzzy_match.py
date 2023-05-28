import pytest

import bionty as bt


@pytest.fixture(scope="session")
def ct():
    return bt.CellType(source="cl", version="2023-02-15")


def test_fuzzy_match_name(ct):
    assert ct.fuzzy_match("T cells", ct.name).index == "T cell"


def test_fuzzy_match_synonyms(ct):
    assert ct.fuzzy_match("P cells", ct.name).index == "nodal myocyte"


def test_fuzzy_match_synonyms_field_none(ct):
    assert ct.fuzzy_match("P cell", ct.name, synonyms_field=None).index == "PP cell"


def test_fuzzy_match_return_ranked_results(ct):
    assert ct.fuzzy_match("P cell", ct.name, return_ranked_results=True).shape == (
        2681,
        5,
    )


def test_fuzzy_match_return_tie_results(ct):
    assert ct.fuzzy_match("A cell", ct.name, synonyms_field=None).shape[0] == 2
