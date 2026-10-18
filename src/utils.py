"""Утилиты для загрузки данных из файлов."""
import json
import os
from typing import Any

import pandas as pd

from src.logger_config import get_logger

logger = get_logger("utils")


def load_transactions(file_path: str) -> list[dict[str, Any]]:
    """Загружает список транзакций из JSON, CSV или XLSX-файла.

    Формат определяется по расширению файла.

    Args:
        file_path: путь к файлу с транзакциями.

    Returns:
        Список словарей с транзакциями. Если файл не найден, пустой,
        содержит не список или содержит некорректные данные — пустой список.
    """
    logger.info(f"Загрузка транзакций из файла: {file_path}")

    if not os.path.exists(file_path):
        logger.error(f"Файл не найден: {file_path}")
        return []

    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".json":
        return _load_from_json(file_path)
    elif ext == ".csv":
        return _load_from_csv(file_path)
    elif ext == ".xlsx":
        return _load_from_xlsx(file_path)
    else:
        logger.warning(f"Неподдерживаемый формат файла: {ext}")
        return []


def _load_from_json(file_path: str) -> list[dict[str, Any]]:
    """Внутренняя функция для чтения JSON."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        logger.error(f"Ошибка при чтении JSON-файла {file_path}: {e}")
        return []

    if not isinstance(data, list):
        logger.warning(f"JSON-файл {file_path} не содержит список. Возвращен пустой список.")
        return []

    logger.info(f"Успешно загружено из JSON транзакций: {len(data)}")
    return data


def _load_from_csv(file_path: str) -> list[dict[str, Any]]:
    """Внутренняя функция для чтения CSV."""
    try:
        df = pd.read_csv(file_path)
        # Превращаем DataFrame в список словарей
        data = df.to_dict(orient="records")
    except Exception as e:
        logger.error(f"Ошибка при чтении CSV-файла {file_path}: {e}")
        return []

    logger.info(f"Успешно загружено из CSV транзакций: {len(data)}")
    return data


def _load_from_xlsx(file_path: str) -> list[dict[str, Any]]:
    """Внутренняя функция для чтения XLSX."""
    try:
        df = pd.read_excel(file_path)
        data = df.to_dict(orient="records")
    except Exception as e:
        logger.error(f"Ошибка при чтении XLSX-файла {file_path}: {e}")
        return []

    logger.info(f"Успешно загружено из XLSX транзакций: {len(data)}")
    return data
