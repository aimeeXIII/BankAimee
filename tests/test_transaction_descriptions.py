import pytest
from generators.transaction_descriptions import transaction_descriptions


class TestTransactionDescriptions:
    """Тесты генератора transaction_descriptions."""

    def test_returns_iterator(self, transactions: list[dict]) -> None:
        """Функция возвращает именно итератор, а не список."""
        result = transaction_descriptions(transactions)
        assert hasattr(result, "__iter__")
        assert hasattr(result, "__next__")
        assert not isinstance(result, list)

    def test_all_descriptions_in_order(
        self,
        transactions: list[dict],
        transaction_descriptions_list: list[str],
    ) -> None:
        """Возвращает описания в исходном порядке."""
        result = list(transaction_descriptions(transactions))
        assert result == transaction_descriptions_list

    def test_next_yields_descriptions_one_by_one(
        self,
        transactions: list[dict],
        transaction_descriptions_list: list[str],
    ) -> None:
        """next() поочерёдно выдаёт описания."""
        iterator = transaction_descriptions(transactions)

        for expected in transaction_descriptions_list:
            assert next(iterator) == expected

        with pytest.raises(StopIteration):
            next(iterator)

    def test_empty_list(self) -> None:
        """Пустой список — пустой итератор."""
        assert list(transaction_descriptions([])) == []

    def test_missing_description_yields_empty_string(self) -> None:
        """Если у транзакции нет description — возвращается пустая строка."""
        data = [
            {"id": 1, "description": "Перевод организации"},
            {"id": 2},  # нет description
            {"id": 3, "description": ""},
        ]
        assert list(transaction_descriptions(data)) == [
            "Перевод организации",
            "",
            "",
        ]

    @pytest.mark.parametrize(
        "descriptions, expected",
        [
            (["A", "B", "C"], ["A", "B", "C"]),
            ([""], [""]),
            ([], []),
        ],
        ids=["three-items", "one-empty", "empty-list"],
    )
    def test_various_inputs(self, descriptions: list[str], expected: list[str]) -> None:
        """Проверяем разные наборы описаний."""
        data = [{"description": d} for d in descriptions]
        assert list(transaction_descriptions(data)) == expected

    def test_lazy_evaluation(self) -> None:
        """Генератор не обходит весь список, пока его не итерируют."""
        calls = {"count": 0}

        class CountingList(list):
            def __iter__(self):
                calls["count"] += 1
                return super().__iter__()

        data = CountingList([
            {"description": "A"},
            {"description": "B"},
            {"description": "C"},
        ])

        iterator = transaction_descriptions(data)
        next(iterator)  # один шаг
        assert calls["count"] <= 1
