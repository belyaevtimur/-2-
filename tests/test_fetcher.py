import pytest
from src.fetcher import load_test_graph


def test_load_simple():
    g = load_test_graph("tests/fixtures/simple.txt")
    assert g["A"] == ["B", "C"]
    assert g["D"] == []


def test_load_missing():
    with pytest.raises(ValueError):
        load_test_graph("nope.txt")
