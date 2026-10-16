import os
from unittest.mock import patch

import pytest

from src.external_api import convert_transaction_to_rub, get_exchange_rate


class TestGetExchangeRate:
    """Тесты функции get_exchange_rate."""

    @patch.dict(os.environ, {"EXCHANGE_RATES_API_KEY": "test_key"})
    @patch("src.external_api.requests.get")
    def test_success(self, mock_get, mock_api_response_success) -> None:
        """Успешный запрос — возвращается курс."""
        mock_get.return_value.json.return_value = mock_api_response_success

        result = get_exchange_rate("USD", "RUB")

        assert result == 90.5
        mock_get.assert_called_once()

    @patch.dict(os.environ, {"EXCHANGE_RATES_API_KEY": "test_key"})
    @patch("src.external_api.requests.get")
    def test_api_error(self, mock_get, mock_api_response_error) -> None:
        """API вернул success=False — ValueError."""
        mock_get.return_value.json.return_value = mock_api_response_error

        with pytest.raises(ValueError, match="Ошибка API"):
            get_exchange_rate("USD", "RUB")

    @patch.dict(os.environ, {}, clear=True)
    def test_missing_api_key(self) -> None:
        """Нет API-ключа — ValueError."""
        with pytest.raises(ValueError, match="EXCHANGE_RATES_API_KEY"):
            get_exchange_rate("USD", "RUB")

    @patch.dict(os.environ, {"EXCHANGE_RATES_API_KEY": "test_key"})
    @patch("src.external_api.requests.get")
    def test_passes_correct_params(self, mock_get, mock_api_response_success) -> None:
        """Проверяем, что запрос уходит с правильными параметрами."""
        mock_get.return_value.json.return_value = mock_api_response_success

        get_exchange_rate("USD", "RUB")

        _, kwargs = mock_get.call_args
        assert kwargs["params"]["from"] == "USD"
        assert kwargs["params"]["to"] == "RUB"
        assert kwargs["headers"]["apikey"] == "test_key"


class TestConvertTransactionToRub:
    """Тесты функции convert_transaction_to_rub."""

    def test_rub_transaction(self, rub_transaction) -> None:
        """RUB — возвращается amount без запросов к API."""
        with patch("src.external_api.get_exchange_rate") as mock_rate:
            result = convert_transaction_to_rub(rub_transaction)

        assert result == 1000.50
        mock_rate.assert_not_called()

    @patch("src.external_api.get_exchange_rate")
    def test_usd_transaction(self, mock_rate, usd_transaction) -> None:
        """USD — конвертация через API."""
        mock_rate.return_value = 90.0

        result = convert_transaction_to_rub(usd_transaction)

        assert result == 9000.0
        mock_rate.assert_called_once_with("USD", "RUB")

    @patch("src.external_api.get_exchange_rate")
    def test_eur_transaction(self, mock_rate, eur_transaction) -> None:
        """EUR — конвертация через API."""
        mock_rate.return_value = 100.0

        result = convert_transaction_to_rub(eur_transaction)

        assert result == 5000.0
        mock_rate.assert_called_once_with("EUR", "RUB")

    def test_unsupported_currency(self) -> None:
        """Неподдерживаемая валюта — ValueError."""
        transaction = {
            "operationAmount": {
                "amount": "100.00",
                "currency": {"name": "GBP", "code": "GBP"},
            }
        }

        with pytest.raises(ValueError, match="Неподдерживаемая валюта"):
            convert_transaction_to_rub(transaction)

    @patch("src.external_api.get_exchange_rate")
    def test_float_conversion(self, mock_rate, usd_transaction) -> None:
        """Возвращается именно float."""
        mock_rate.return_value = 90.5

        result = convert_transaction_to_rub(usd_transaction)

        assert isinstance(result, float)
        assert result == 9050.0
