"""Построение графа зависимостей: BFS без рекурсии, обратные зависимости."""
from collections import deque
from typing import Callable, Dict, List, Optional, Set


def build_graph_bfs(
    root: str,
    get_deps: Callable[[str], List[str]],
    max_depth: int,
) -> Dict[str, Set[str]]:
    """BFS без рекурсии (требование этапа 3).

    Возвращает граф вида {узел: {зависимости}}.
    Корректно обрабатывает циклы: узел обрабатывается один раз.
    """
    graph: Dict[str, Set[str]] = {}
    visited: Set[str] = set()
    queue: deque = deque([(root, 0)])

    while queue:
        node, depth = queue.popleft()
        if node in visited:
            continue
        visited.add(node)
        graph.setdefault(node, set())

        if depth >= max_depth:
            continue

        try:
            deps = get_deps(node)
        except ValueError:
            deps = []

        for dep in deps:
            graph[node].add(dep)
            if dep not in visited:
                queue.append((dep, depth + 1))

    return graph


def reverse_graph(graph: Dict[str, Set[str]]) -> Dict[str, Set[str]]:
    """Инвертирует граф: для узла — кто от него зависит."""
    reversed_g: Dict[str, Set[str]] = {node: set() for node in graph}
    for node, deps in graph.items():
        for dep in deps:
            reversed_g.setdefault(dep, set()).add(node)
    return reversed_g


def find_reverse_dependencies(
    target: str, graph: Dict[str, Set[str]], max_depth: int
) -> Set[str]:
    """Обратные зависимости (этап 4): пакеты, зависящие от target.

    Обход — BFS по инвертированному графу, без рекурсии.
    """
    reversed_g = reverse_graph(graph)
    result: Set[str] = set()
    visited: Set[str] = {target}
    queue: deque = deque([(target, 0)])

    while queue:
        node, depth = queue.popleft()
        if depth >= max_depth:
            continue
        for parent in reversed_g.get(node, ()):
            if parent not in visited:
                visited.add(parent)
                result.add(parent)
                queue.append((parent, depth + 1))
    return result
