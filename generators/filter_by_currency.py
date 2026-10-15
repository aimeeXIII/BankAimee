from typing import Any, Iterator


def filter_by_currency(
    transactions: list[dict[str, Any]],
    currency_code: str,
) -> Iterator[dict[str, Any]]:
    """Возвращает итератор по транзакциям с указанной валютой.

    Args:
        transactions: список словарей с транзакциями.
        currency_code: код валюты (например, "USD", "RUB").

    Yields:
        Транзакции, у которых operationAmount.currency.code == currency_code.
    """
    for transaction in transactions:
        try:
            code = transaction["operationAmount"]["currency"]["code"]
        except (KeyError, TypeError):
            # пропускаем «кривые» транзакции, не падая
            continue

        if code == currency_code:
            yield transaction
