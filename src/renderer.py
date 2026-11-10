"""Визуализация графа в D2 и сохранение в SVG (этап 5)."""
import subprocess
from typing import Dict, Set


def to_d2(graph: Dict[str, Set[str]]) -> str:
    """Формирует текстовое представление графа на языке D2."""
    lines = ["direction: right", ""]
    for node, deps in graph.items():
        if not deps:
            lines.append(f'"{node}"')
        for dep in deps:
            lines.append(f'"{node}" -> "{dep}"')
    return "\n".join(lines)


def save_svg(d2_source: str, output_file: str) -> None:
    """Сохраняет SVG через d2 CLI."""
    try:
        subprocess.run(
            ["d2", "-", output_file],
            input=d2_source.encode("utf-8"),
            check=True,
        )
    except FileNotFoundError:
        raise ValueError(
            "d2 не установлен. Установите: https://d2lang.com/tour/install"
        )
    except subprocess.CalledProcessError as e:
        raise ValueError(f"Ошибка d2: {e}")
