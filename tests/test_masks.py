import pytest
from src.masks import get_mask_card_number, get_mask_account


class TestGetMaskCardNumber:
    def test_standard_card(self):
        assert get_mask_card_number("1234567812345678") == "1234 56** **** 5678"

    def test_card_with_spaces(self):
        assert get_mask_card_number("1234 5678 1234 5678") == "1234 56** **** 5678"

    def test_card_first_and_last_four(self):
        assert get_mask_card_number("1111222233334444") == "1111 22** **** 4444"

    def test_card_repeated_digits(self):
        assert get_mask_card_number("0000000000000000") == "0000 00** **** 0000"

    def test_short_number(self):
        assert get_mask_card_number("1234") == "1234 ** **** 1234"


class TestGetMaskAccount:
    def test_standard_account(self):
        assert get_mask_account("73654108430135874305") == "**4305"

    def test_short_account(self):
        assert get_mask_account("1234") == "**1234"

    def test_account_less_than_four(self):
        assert get_mask_account("12") == "**12"

    def test_account_repeated_digits(self):
        assert get_mask_account("0000000000") == "**0000"