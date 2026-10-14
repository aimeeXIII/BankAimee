from typing import Any, Dict, List


def filter_by_state(data: List[Dict[str, Any]], state_value: str = "EXECUTED") -> List[Dict[str, Any]]:
    """Фильтрует список словарей по значению ключа 'state'."""
    return [item for item in data if item.get("state") == state_value]

def sort_by_date(data: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    """Сортирует список словарей по дате. По умолчанию сортировка идет по убыванию."""
    return sorted(data, key=lambda item: item.get("date", ""), reverse=reverse)
