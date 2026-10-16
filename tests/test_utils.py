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
