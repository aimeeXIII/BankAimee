"""Утилиты для загрузки данных из файлов."""
import json
from typing import Any


def load_transactions(file_path: str) -> list[dict[str, Any]]:
    """Загружает список транзакций из JSON-файла.

    Args:
        file_path: путь к JSON-файлу с транзакциями.

    Returns:
        Список словарей с транзакциями. Если файл не найден, пустой,
        содержит не список или содержит некорректный JSON — пустой список.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return []

    if not isinstance(data, list):
        return []

    return data
