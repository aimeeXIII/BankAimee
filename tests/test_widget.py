import pytest
from src.widget import mask_account_card, get_date


class TestMaskAccountCard:
    def test_card_visa(self):
        assert mask_account_card("Visa Platinum 1234567812345678") == "Visa Platinum 1234 56** **** 5678"

    def test_account_uppercase(self):
        assert mask_account_card("Счет 73654108430135874305") == "Счет **4305"

    def test_account_lowercase(self):
        assert mask_account_card("счет 12345678901234567890") == "счет **7890"

    def test_card_with_spaces_in_name(self):
        assert mask_account_card("Visa Gold Premium 1111222233334444") == "Visa Gold Premium 1111 22** **** 4444"

    def test_extra_spaces(self):
        assert mask_account_card("  Visa   1234567812345678  ") == "Visa 1234 56** **** 5678"

    def test_empty_string_raises(self):
        with pytest.raises(IndexError):
            mask_account_card("")


class TestGetDate:
    def test_standard_iso(self):
        assert get_date("2024-03-15T10:30:00") == "15.03.2024"

    def test_only_date(self):
        assert get_date("2023-12-31") == "31.12.2023"

    def test_with_timezone(self):
        assert get_date("2022-01-01T00:00:00+03:00") == "01.01.2022"

    def test_leap_year(self):
        assert get_date("2024-02-29T23:59:59") == "29.02.2024"

    def test_empty_string(self):
        assert get_date("") == ".."