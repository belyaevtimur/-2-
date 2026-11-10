"""Точка входа CLI-приложения."""
import sys
from .config import load_config, print_config
from .fetcher import fetch_dependencies_real, load_test_graph
from .graph import build_graph_bfs, find_reverse_dependencies
from .renderer import to_d2, save_svg
from .ascii_tree import render_ascii_tree


def main(argv):
    if len(argv) != 2:
        print("Использование: python -m src.main <config.json>")
        return 1

    # Этап 1: вывод всех параметров
    try:
        cfg = load_config(argv[1])
    except ValueError as e:
        print(f"Ошибка конфигурации: {e}", file=sys.stderr)
        return 1
    print("=== Параметры ===")
    print_config(cfg)
    print()

    # Этап 2: получение прямых зависимостей
    if cfg.test_mode:
        full_graph = load_test_graph(cfg.repo_url)
        def get_deps(node: str):
            return full_graph.get(node, [])
    else:
        def get_deps(node: str):
            return fetch_dependencies_real(cfg.repo_url, node, cfg.version)

    print("=== Прямые зависимости ===")
    try:
        direct = get_deps(cfg.package)
    except ValueError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        return 1
    for d in direct:
        print(f"  {d}")
    print()

    # Этап 3: граф BFS
    graph = build_graph_bfs(cfg.package, get_deps, cfg.max_depth)

    # Этап 4: обратные зависимости
    print("=== Обратные зависимости ===")
    reverse = find_reverse_dependencies(cfg.package, graph, cfg.max_depth)
    for r in sorted(reverse):
        print(f"  {r}")
    print()

    # Этап 5: визуализация
    d2_source = to_d2(graph)
    try:
        save_svg(d2_source, cfg.output_file)
        print(f"Граф сохранён: {cfg.output_file}")
    except ValueError as e:
        print(f"Предупреждение: {e}", file=sys.stderr)

    if cfg.ascii_tree:
        print("\n=== ASCII-дерево ===")
        print(render_ascii_tree(cfg.package, graph))

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
