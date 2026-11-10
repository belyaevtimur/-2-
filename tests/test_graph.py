from src.graph import build_graph_bfs, find_reverse_dependencies


def test_bfs_linear():
    deps = {"A": ["B"], "B": ["C"], "C": []}
    g = build_graph_bfs("A", lambda n: deps.get(n, []), max_depth=5)
    assert g["A"] == {"B"}
    assert g["C"] == set()


def test_bfs_depth_limit():
    deps = {"A": ["B"], "B": ["C"], "C": ["D"], "D": []}
    g = build_graph_bfs("A", lambda n: deps.get(n, []), max_depth=1)
    assert "C" not in g


def test_bfs_cycle():
    deps = {"A": ["B"], "B": ["C"], "C": ["A"]}
    g = build_graph_bfs("A", lambda n: deps.get(n, []), max_depth=10)
    assert "A" in g["C"]


def test_reverse_deps():
    deps = {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}
    g = build_graph_bfs("A", lambda n: deps.get(n, []), max_depth=5)
    rev = find_reverse_dependencies("D", g, max_depth=5)
    assert "B" in rev and "C" in rev
