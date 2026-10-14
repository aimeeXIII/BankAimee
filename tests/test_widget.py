import pytest
from src.widget import mask_account_card, get_date


class TestMaskAccountCard:
    """Тесты комплексной маскировки 'тип + номер'."""

    @pytest.mark.parametrize(
        "info_string, expected",
        [
            # --- карты ---
            ("Visa Platinum 1234567812345678", "Visa Platinum 1234 56** **** 5678"),
            ("MasterCard 5678901234565678", "MasterCard 5678 90** **** 5678"),
            ("Maestro 1111222233334444", "Maestro 1111 22** **** 4444"),
            ("Visa Gold Premium 1111222233334444", "Visa Gold Premium 1111 22** **** 4444"),
            ("1234567812345678", " 1234 56** **** 5678"),  # без имени
            ("  Visa   1234567812345678  ", "Visa 1234 56** **** 5678"),  # лишние пробелы

            # --- счета (регистронезависимо) ---
            ("Счет 73654108430135874305", "Счет **4305"),
            ("счет 12345678901234567890", "счет **7890"),
            ("СчЕт 12345678901234567890", "СчЕт **7890"),
        ]
    )
    def test_mask_account_card(self, info_string: str, expected: str) -> None:
        assert mask_account_card(info_string) == expected

    def test_empty_string_raises(self) -> None:
        """Пустая строка -> IndexError (parts[-1] не существует)."""
        with pytest.raises(IndexError):
            mask_account_card("")

    def test_card_fixture(self, card_info_string: str) -> None:
        assert mask_account_card(card_info_string) == "Visa Platinum 1234 56** **** 5678"

    def test_account_fixture(self, account_info_string: str) -> None:
        assert mask_account_card(account_info_string) == "Счет **4305"


class TestGetDate:
    """Тесты преобразования ISO-даты в ДД.ММ.ГГГГ."""

    @pytest.mark.parametrize(
        "date_string, expected",
        [
            ("2024-03-15T10:30:00", "15.03.2024"),            # стандарт
            ("2023-12-31", "31.12.2023"),                     # только дата
            ("2022-01-01T00:00:00+03:00", "01.01.2022"),      # с таймзоной
            ("2021-07-04T12:34:56.789012", "04.07.2021"),     # с микросекундами
            ("2020-01-05T00:00:00", "05.01.2020"),            # однозначные м/д
            ("2024-02-29T23:59:59", "29.02.2024"),            # високосный
            ("2023-12-31T23:59:59", "31.12.2023"),            # конец года
        ]
    )
    def test_get_date(self, date_string: str, expected: str) -> None:
        assert get_date(date_string) == expected

    @pytest.mark.parametrize(
        "date_string, expected",
        [
            ("", ".."),             # пустая строка
            ("2024-03", ".03.2024"),  # слишком короткая
        ]
    )
    def test_get_date_edge_cases(self, date_string: str, expected: str) -> None:
        """Фиксируем текущее поведение на некорректных данных."""
        assert get_date(date_string) == expected

    def test_iso_datetime_fixture(self, iso_datetime_string: str) -> None:
        assert get_date(iso_datetime_string) == "15.03.2024"
