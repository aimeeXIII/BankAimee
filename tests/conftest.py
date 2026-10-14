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


@pytest.fixture
def transactions() -> list[dict]:
    """Набор разнообразных транзакций для тестов filter_by_currency."""
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {"name": "руб.", "code": "RUB"},
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160",
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {
                "amount": "67314.70",
                "currency": {"name": "руб.", "code": "RUB"},
            },
            "description": "Перевод организации",
            "from": "Счет 65098000801316618210",
            "to": "Счет 60381795328933286458",
        },
        {
            "id": 615064591,
            "state": "CANCELED",
            "date": "2018-10-14T08:21:33.419441",
            "operationAmount": {
                "amount": "77751.04",
                "currency": {"name": "руб.", "code": "RUB"},
            },
            "description": "Перевод с карты на счет",
            "from": "Maestro 3928549031574026",
            "to": "Счет 84163357546688983493",
        },
    ]


@pytest.fixture
def usd_transactions(transactions: list[dict]) -> list[dict]:
    """Только USD-транзакции из общего списка (для проверки)."""
    return [t for t in transactions if t["operationAmount"]["currency"]["code"] == "USD"]


@pytest.fixture
def rub_transactions(transactions: list[dict]) -> list[dict]:
    """Только RUB-транзакции из общего списка (для проверки)."""
    return [t for t in transactions if t["operationAmount"]["currency"]["code"] == "RUB"]


@pytest.fixture
def broken_transactions() -> list[dict]:
    """Набор с «кривыми» транзакциями: без operationAmount, currency и т.п."""
    return [
        {"id": 1, "state": "EXECUTED"},                              # нет operationAmount
        {"id": 2, "operationAmount": {}},                            # нет currency
        {"id": 3, "operationAmount": {"currency": {}}},              # нет code
        {"id": 4, "operationAmount": {"currency": {"code": "USD"}}}, # корректная USD
    ]