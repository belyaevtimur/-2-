"""Загрузка и валидация JSON-конфигурации."""
import json
from dataclasses import dataclass


@dataclass
class Config:
    package: str
    repo_url: str
    test_mode: bool
    version: str
    output_file: str
    ascii_tree: bool
    max_depth: int


REQUIRED_KEYS = {
    "package": str,
    "repo_url": str,
    "test_mode": bool,
    "version": str,
    "output_file": str,
    "ascii_tree": bool,
    "max_depth": int,
}


def load_config(path: str) -> Config:
    """Читает JSON-файл и валидирует все параметры."""
    try:
        with open(path, encoding="utf-8") as f:
            raw = json.load(f)
    except FileNotFoundError:
        raise ValueError(f"Файл конфигурации не найден: {path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Некорректный JSON: {e}")

    if not isinstance(raw, dict):
        raise ValueError("Корень конфигурации должен быть объектом JSON")

    for key, expected_type in REQUIRED_KEYS.items():
        if key not in raw:
            raise ValueError(f"Отсутствует обязательный ключ: {key}")
        if not isinstance(raw[key], expected_type):
            raise ValueError(
                f"Ключ '{key}' должен быть типа {expected_type.__name__}"
            )

    if not raw["package"].strip():
        raise ValueError("Имя пакета не может быть пустым")
    if raw["max_depth"] < 0:
        raise ValueError("max_depth должен быть неотрицательным")
    if not raw["version"].strip():
        raise ValueError("Версия не может быть пустой")

    return Config(**raw)


def print_config(cfg: Config) -> None:
    """Вывод параметров в формате ключ-значение (требование этапа 1)."""
    for field, value in cfg.__dict__.items():
        print(f"{field}: {value}")
