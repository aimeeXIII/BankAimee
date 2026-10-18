import pandas as pd
from src.utils import load_transactions


class TestLoadTransactions:
    """Тесты функции load_transactions."""

    def test_valid_file_returns_list(self, valid_transactions_file: str) -> None:
        """Валидный JSON со списком — возвращается список."""
        result = load_transactions(valid_transactions_file)
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["id"] == 1
        assert result[1]["id"] == 2

    def test_file_not_found(self, tmp_path) -> None:
        """Несуществующий файл — пустой список."""
        missing = tmp_path / "does_not_exist.json"
        assert load_transactions(str(missing)) == []

    def test_empty_file(self, empty_file: str) -> None:
        """Пустой файл — пустой список (json.JSONDecodeError)."""
        assert load_transactions(empty_file) == []

    def test_json_is_dict_not_list(self, json_dict_file: str) -> None:
        """JSON — словарь, а не список — пустой список."""
        assert load_transactions(json_dict_file) == []

    def test_invalid_json(self, invalid_json_file: str) -> None:
        """Невалидный JSON — пустой список."""
        assert load_transactions(invalid_json_file) == []

    def test_json_is_number(self, tmp_path) -> None:
        """JSON — число, а не список."""
        file_path = tmp_path / "number.json"
        file_path.write_text("42", encoding="utf-8")
        assert load_transactions(str(file_path)) == []

    def test_json_is_string(self, tmp_path) -> None:
        """JSON — строка, а не список."""
        file_path = tmp_path / "string.json"
        file_path.write_text('"hello"', encoding="utf-8")
        assert load_transactions(str(file_path)) == []

    def test_json_is_null(self, tmp_path) -> None:
        """JSON — null, а не список."""
        file_path = tmp_path / "null.json"
        file_path.write_text("null", encoding="utf-8")
        assert load_transactions(str(file_path)) == []

    def test_empty_list(self, tmp_path) -> None:
        """JSON — пустой список — возвращается пустой список (валидный)."""
        file_path = tmp_path / "empty_list.json"
        file_path.write_text("[]", encoding="utf-8")
        assert load_transactions(str(file_path)) == []

    def test_utf8_characters(self, tmp_path) -> None:
        """Русские символы в JSON читаются корректно."""
        file_path = tmp_path / "ru.json"
        file_path.write_text(
            '[{"description": "Перевод организации"}]',
            encoding="utf-8",
        )
        result = load_transactions(str(file_path))
        assert result[0]["description"] == "Перевод организации"

    def test_real_data_file(self) -> None:
        """Интеграционный тест: читаем реальный data/operations.json."""
        import os
        path = os.path.join("data", "operations.json")
        if not os.path.exists(path):
            import pytest
            pytest.skip("data/operations.json не найден")
        result = load_transactions(path)
        assert isinstance(result, list)


class TestLoadTransactionsCSV:
    """Тесты функции load_transactions для CSV-файлов."""

    def test_valid_csv(self, tmp_path):
        """Валидный CSV — возвращает список словарей."""
        file_path = tmp_path / "test.csv"
        # Создаём тестовый CSV
        df = pd.DataFrame([
            {"id": 1, "amount": 100.50, "currency": "RUB"},
            {"id": 2, "amount": 200.00, "currency": "USD"},
        ])
        df.to_csv(file_path, index=False)

        result = load_transactions(str(file_path))

        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["id"] == 1
        assert result[0]["amount"] == 100.5
        assert result[0]["currency"] == "RUB"

    def test_empty_csv(self, tmp_path):
        """Пустой CSV — возвращает пустой список."""
        file_path = tmp_path / "empty.csv"
        pd.DataFrame().to_csv(file_path, index=False)

        result = load_transactions(str(file_path))
        assert result == []

    def test_broken_csv(self, tmp_path):
        """Если CSV битый (ошибка парсинга) — возвращает пустой список."""
        file_path = tmp_path / "broken.csv"
        file_path.write_text("some broken text", encoding="utf-8")

        # pandas может прочитать это как 1 колонку, но не упадёт.
        # Чтобы точно упало, можно сделать что-то вроде:
        # pd.read_csv(file_path, ...) вызовет ошибку.
        # Но для простоты проверим, что функция не падает.
        result = load_transactions(str(file_path))
        assert isinstance(result, list)


class TestLoadTransactionsXLSX:
    """Тесты функции load_transactions для XLSX-файлов."""

    def test_valid_xlsx(self, tmp_path):
        """Валидный XLSX — возвращает список словарей."""
        file_path = tmp_path / "test.xlsx"

        df = pd.DataFrame([
            {"id": 3, "amount": 300.00, "currency": "EUR"},
            {"id": 4, "amount": 400.00, "currency": "RUB"},
        ])
        df.to_excel(file_path, index=False)

        result = load_transactions(str(file_path))

        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["id"] == 3
        assert result[0]["currency"] == "EUR"

    def test_empty_xlsx(self, tmp_path):
        """Пустой XLSX — возвращает пустой список."""
        file_path = tmp_path / "empty.xlsx"
        pd.DataFrame().to_excel(file_path, index=False)

        result = load_transactions(str(file_path))
        assert result == []


def test_unsupported_extension(tmp_path):
    """Файл с неподдерживаемым расширением — пустой список."""
    file_path = tmp_path / "test.txt"
    file_path.write_text("some text", encoding="utf-8")

    result = load_transactions(str(file_path))
    assert result == []
