"""Модуль для работы с внешним API конвертации валют."""
import os
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()  # загружаем переменные из .env при импорте

API_URL = "https://api.apilayer.com/exchangerates_data/convert"


def get_exchange_rate(from_currency: str, to_currency: str) -> float:
    """Получает текущий курс конвертации через Exchange Rates Data API.

    Args:
        from_currency: код исходной валюты (например, "USD").
        to_currency: код целевой валюты (например, "RUB").

    Returns:
        Курс конвертации (float).

    Raises:
        ValueError: если API-ключ не задан или API вернул ошибку.
    """
    api_key = os.getenv("EXCHANGE_RATES_API_KEY")
    if not api_key:
        raise ValueError("EXCHANGE_RATES_API_KEY не задан в .env")

    headers = {"apikey": api_key}
    params = {"from": from_currency, "to": to_currency, "amount": 1}

    response = requests.get(API_URL, headers=headers, params=params, timeout=10)
    data: dict[str, Any] = response.json()

    if not data.get("success"):
        raise ValueError(f"Ошибка API: {data.get('error', 'unknown')}")

    return float(data["result"])


def convert_transaction_to_rub(transaction: dict[str, Any]) -> float:
    """Возвращает сумму транзакции в рублях.

    Для RUB — возвращает amount как float.
    Для USD/EUR — конвертирует через внешний API.

    Args:
        transaction: словарь с ключом operationAmount.

    Returns:
        Сумма в рублях (float).

    Raises:
        ValueError: если валюта не поддерживается или API вернул ошибку.
    """
    amount_info = transaction["operationAmount"]
    amount = float(amount_info["amount"])
    currency_code = amount_info["currency"]["code"]

    if currency_code == "RUB":
        return amount

    if currency_code in ("USD", "EUR"):
        rate = get_exchange_rate(currency_code, "RUB")
        return amount * rate

    raise ValueError(f"Неподдерживаемая валюта: {currency_code}")
