import pytest


@pytest.fixture
def valid_card_number() -> str:
    """Стандартный 16-значный номер карты без пробелов."""
    return "1234567812345678"


@pytest.fixture
def valid_card_number_with_spaces() -> str:
    """Номер карты с пробелами (формат отображения)."""
    return "1234 5678 1234 5678"


@pytest.fixture
def valid_account_number() -> str:
    """Стандартный 20-значный номер счёта."""
    return "73654108430135874305"



@pytest.fixture
def card_info_string() -> str:
    """Строка вида '<Название карты> <номер>'."""
    return "Visa Platinum 1234567812345678"


@pytest.fixture
def account_info_string() -> str:
    """Строка вида 'Счет <номер>'."""
    return "Счет 73654108430135874305"


@pytest.fixture
def iso_datetime_string() -> str:
    """Строка даты в формате ISO с временем."""
    return "2024-03-15T10:30:00"