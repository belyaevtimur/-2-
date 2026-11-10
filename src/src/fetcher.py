"""Получение прямых зависимостей пакета Rust.

Реальный режим — HTTP-запрос к crates.io API (без cargo/npm-библиотек).
Тестовый режим — чтение графа из файла.
"""
import urllib.request
import json
from typing import Dict, List


def fetch_dependencies_real(
    repo_url: str, package: str, version: str
) -> List[str]:
    """Возвращает список имён прямых зависимостей пакета.

    Использует публичный API crates.io: /api/v1/crates/{name}/{version}/dependencies
    """
    url = f"{repo_url.rstrip('/')}/{package}/{version}/dependencies"
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise ValueError(f"Ошибка HTTP {e.code} при запросе {url}")
    except Exception as e:
        raise ValueError(f"Не удалось получить зависимости: {e}")

    deps = data.get("dependencies", [])
    return [d["crate_id"] for d in deps]


def load_test_graph(path: str) -> Dict[str, List[str]]:
    """Читает граф из файла.

    Формат строки: A: B C D   (пакеты — заглавные латинские буквы)
    """
    graph: Dict[str, List[str]] = {}
    try:
        with open(path, encoding="utf-8") as f:
            for lineno, line in enumerate(f, 1):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if ":" not in line:
                    raise ValueError(f"Строка {lineno}: нет ':'")
                node, deps = line.split(":", 1)
                node = node.strip()
                dep_list = deps.split()
                if not node.isalpha() or not node.isupper():
                    raise ValueError(
                        f"Строка {lineno}: имя пакета должно быть заглавными буквами"
                    )
                graph[node] = dep_list
    except FileNotFoundError:
        raise ValueError(f"Файл тестового графа не найден: {path}")
    return graph
