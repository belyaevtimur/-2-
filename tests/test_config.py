import json, tempfile, os
import pytest
from src.config import load_config


def _write(data):
    fd, path = tempfile.mkstemp(suffix=".json")
    with os.fdopen(fd, "w") as f:
        json.dump(data, f)
    return path


def test_valid():
    p = _write({
        "package": "serde", "repo_url": "u", "test_mode": False,
        "version": "1.0.0", "output_file": "g.svg",
        "ascii_tree": True, "max_depth": 3,
    })
    cfg = load_config(p)
    assert cfg.package == "serde"
    assert cfg.max_depth == 3


def test_missing_key():
    p = _write({"package": "a"})
    with pytest.raises(ValueError):
        load_config(p)


def test_bad_type():
    p = _write({
        "package": "a", "repo_url": "u", "test_mode": "yes",
        "version": "1", "output_file": "g", "ascii_tree": True,
        "max_depth": 1,
    })
    with pytest.raises(ValueError):
        load_config(p)


def test_negative_depth():
    p = _write({
        "package": "a", "repo_url": "u", "test_mode": False,
        "version": "1", "output_file": "g", "ascii_tree": True,
        "max_depth": -1,
    })
    with pytest.raises(ValueError):
        load_config(p)
