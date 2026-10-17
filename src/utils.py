"""Утилиты для загрузки данных из файлов."""
import json
from typing import Any

from src.logger_config import get_logger

logger = get_logger("utils")


def load_transactions(file_path: str) -> list[dict[str, Any]]:
    """Загружает список транзакций из JSON-файла.

    Args:
        file_path: путь к JSON-файлу с транзакциями.

    Returns:
        Список словарей с транзакциями. Если файл не найден, пустой,
        содержит не список или содержит некорректный JSON — пустой список.
    """
    logger.info(f"Загрузка транзакций из файла: {file_path}")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, OSError) as e:
        logger.error(f"Ошибка при чтении файла {file_path}: {e}")
        return []

    if not isinstance(data, list):
        logger.warning(f"Файл {file_path} не содержит список. Возвращен пустой список.")
        return []

    logger.info(f"Успешно загружено транзакций: {len(data)}")
    return data
