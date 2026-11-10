"""Вывод зависимостей в виде ASCII-дерева (этап 5, параметр ascii_tree)."""
from typing import Dict, Set


def render_ascii_tree(
    node: str, graph: Dict[str, Set[str]], prefix: str = "",
    visited: Set[str] = None
) -> str:
    """Рекурсивный вывод дерева. Циклы помечаются '(cycle)'."""
    if visited is None:
        visited = set()
    lines = [f"{prefix}{node}"]
    if node in visited:
        lines[0] += " (cycle)"
        return "\n".join(lines)
    visited.add(node)
    children = sorted(graph.get(node, ()))
    for i, child in enumerate(children):
        connector = "└── " if i == len(children) - 1 else "├── "
        extension = "    " if i == len(children) - 1 else "│   "
        lines.append(
            render_ascii_tree(child, graph, prefix + connector, visited)
        )
        # переоткрываем узел для ветвления (не помечаем как цикл)
        visited.discard(child)
    return "\n".join(lines)
