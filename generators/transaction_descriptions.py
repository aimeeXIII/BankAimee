from typing import Any, Iterator


def transaction_descriptions(
    transactions: list[dict[str, Any]],
) -> Iterator[str]:
    """Возвращает итератор с описаниями транзакций по очереди.

    Args:
        transactions: список словарей с транзакциями.

    Yields:
        Описание каждой транзакции (поле "description").
        Если поля нет — пустая строка.
    """
    for transaction in transactions:
        yield transaction.get("description", "")