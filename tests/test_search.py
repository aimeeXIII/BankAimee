import pytest
from src.search import process_bank_operations, process_bank_search


@pytest.fixture
def data():
    return [
        {"description": "Перевод организации"},
        {"description": "Перевод со счета на счет"},
        {"description": "Перевод с карты на карту"},
        {"description": "Открытие вклада"},
        {"description": ""},
    ]


class TestProcessBankSearch:
    def test_search_existing(self, data):
        result = process_bank_search(data, "Перевод")
        assert len(result) == 3

    def test_search_case_insensitive(self, data):
        result = process_bank_search(data, "перевод")
        assert len(result) == 3

    def test_search_no_results(self, data):
        result = process_bank_search(data, "тест")
        assert result == []

    def test_search_empty_string(self, data):
        result = process_bank_search(data, "")
        assert result == data

    def test_search_regex_special_chars(self, data):
        # Проверка, что спецсимволы не ломают регулярку (благодаря re.escape)
        result = process_bank_search(data, ".*")
        assert len(result) == 0


class TestProcessBankOperations:
    def test_counts(self, data):
        categories = ["Перевод организации", "Перевод со счета на счет", "Открытие вклада"]
        result = process_bank_operations(data, categories)
        assert result == {
            "Перевод организации": 1,
            "Перевод со счета на счет": 1,
            "Открытие вклада": 1,
        }

    def test_empty_categories(self, data):
        result = process_bank_operations(data, [])
        assert result == {}

    def test_non_existent_category(self, data):
        result = process_bank_operations(data, ["Неизвестная категория"])
        assert result == {"Неизвестная категория": 0}
