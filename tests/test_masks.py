import pytest
from src.masks import get_mask_card_number, get_mask_account


class TestGetMaskCardNumber:
    """Тесты маскирования номера карты."""

    @pytest.mark.parametrize(
        "card_number, expected",
        [
            # (входные данные, ожидаемый результат)
            ("1234567812345678", "1234 56** **** 5678"),  # стандарт
            ("1234 5678 1234 5678", "1234 56** **** 5678"),  # с пробелами
            ("1111222233334444", "1111 22** **** 4444"),  # другие цифры
            ("0000000000000000", "0000 00** **** 0000"),  # все нули
            ("1234", "1234 ** **** 1234"),  # короткий номер
        ]
    )
    def test_mask_card(self, card_number: str, expected: str) -> None:
        assert get_mask_card_number(card_number) == expected

    def test_uses_fixture(self, valid_card_number: str) -> None:
        """Демонстрация использования фикстуры."""
        assert get_mask_card_number(valid_card_number) == "1234 56** **** 5678"

    def test_fixture_with_spaces(self, valid_card_number_with_spaces: str) -> None:
        assert get_mask_card_number(valid_card_number_with_spaces) == "1234 56** **** 5678"


class TestGetMaskAccount:
    """Тесты маскирования номера счёта."""

    @pytest.mark.parametrize(
        "account_number, expected",
        [
            ("73654108430135874305", "**4305"),  # стандарт
            ("1234", "**1234"),                  # ровно 4
            ("12", "**12"),                      # меньше 4
            ("0000000000", "**0000"),            # нули
        ]
    )
    def test_mask_account(self, account_number: str, expected: str) -> None:
        assert get_mask_account(account_number) == expected

    def test_uses_fixture(self, valid_account_number: str) -> None:
        assert get_mask_account(valid_account_number) == "**4305"
