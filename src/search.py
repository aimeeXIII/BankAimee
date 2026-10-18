import re
from collections import Counter
from typing import Any


def process_bank_search(data: list[dict[str, Any]], search: str) -> list[dict[str, Any]]:
    """Ищет транзакции, в описании которых есть подстрока search (без учёта регистра).

    Использует регулярные выражения.
    """
    if not search:
        return data

    # Экранируем спецсимволы, чтобы поиск работал как обычная строка
    pattern = re.compile(re.escape(search), re.IGNORECASE)
    return [t for t in data if pattern.search(t.get("description", ""))]


def process_bank_operations(data: list[dict[str, Any]], categories: list[str]) -> dict[str, int]:
    """Считает количество операций для каждой категории из списка.

    Категория берётся из поля description.
    """
    counts = Counter()
    for transaction in data:
        desc = transaction.get("description", "")
        if desc in categories:
            counts[desc] += 1

    # Возвращаем словарь, где для каждой категории есть ключ (даже если 0)
    return {category: counts[category] for category in categories}
