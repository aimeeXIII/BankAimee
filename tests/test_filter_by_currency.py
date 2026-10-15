import pytest
from generators.filter_by_currency import filter_by_currency


class TestFilterByCurrency:
    """Тесты функции filter_by_currency."""

    def test_returns_iterator(self, transactions: list[dict]) -> None:
        """Функция возвращает именно итератор, а не список."""
        result = filter_by_currency(transactions, "USD")
        assert hasattr(result, "__iter__")
        assert hasattr(result, "__next__")
        # проверим, что это не список
        assert not isinstance(result, list)

    def test_usd_transactions(self, transactions: list[dict], usd_transactions: list[dict]) -> None:
        """Возвращает только USD-транзакции."""
        result = list(filter_by_currency(transactions, "USD"))
        assert result == usd_transactions
        assert len(result) == 2

    def test_rub_transactions(self, transactions: list[dict], rub_transactions: list[dict]) -> None:
        """Возвращает только RUB-транзакции."""
        result = list(filter_by_currency(transactions, "RUB"))
        assert result == rub_transactions
        assert len(result) == 3

    def test_unknown_currency(self, transactions: list[dict]) -> None:
        """Несуществующая валюта — итератор пуст."""
        result = list(filter_by_currency(transactions, "EUR"))
        assert result == []

    def test_empty_list(self) -> None:
        """Пустой список — пустой итератор."""
        result = list(filter_by_currency([], "USD"))
        assert result == []

    def test_next_returns_transactions_in_order(
        self, transactions: list[dict], usd_transactions: list[dict]
    ) -> None:
        """next() поочерёдно выдаёт транзакции в исходном порядке."""
        iterator = filter_by_currency(transactions, "USD")

        first = next(iterator)
        second = next(iterator)

        assert first == usd_transactions[0]
        assert second == usd_transactions[1]

        with pytest.raises(StopIteration):
            next(iterator)

    def test_does_not_modify_input(self, transactions: list[dict]) -> None:
        """Функция не должна мутировать исходный список."""
        snapshot = [dict(t) for t in transactions]  # поверхностная копия
        list(filter_by_currency(transactions, "USD"))
        assert transactions == snapshot

    @pytest.mark.parametrize(
        "currency_code",
        ["USD", "RUB"],
        ids=["usd", "rub"],
    )
    def test_returns_only_matching(
        self, transactions: list[dict], currency_code: str
    ) -> None:
        """Все возвращённые транзакции имеют запрошенный код валюты."""
        for transaction in filter_by_currency(transactions, currency_code):
            assert transaction["operationAmount"]["currency"]["code"] == currency_code

    @pytest.mark.parametrize(
        "currency_code, expected_count",
        [("USD", 2), ("RUB", 3), ("EUR", 0), ("usd", 0)],
        ids=["usd-2", "rub-3", "eur-0", "lowercase-usd-0"],
    )
    def test_counts(
        self, transactions: list[dict], currency_code: str, expected_count: int
    ) -> None:
        """Проверяем количество совпадений для разных валют."""
        result = list(filter_by_currency(transactions, currency_code))
        assert len(result) == expected_count


class TestFilterByCurrencyBrokenData:
    """Проверка устойчивости к «кривым» транзакциям."""

    def test_skips_broken_transactions(self, broken_transactions: list[dict]) -> None:
        """Транзакции без нужных полей пропускаются, корректные — возвращаются."""
        result = list(filter_by_currency(broken_transactions, "USD"))
        assert len(result) == 1
        assert result[0]["id"] == 4

    def test_all_broken_returns_empty(self) -> None:
        """Если все транзакции «кривые» — итератор пуст."""
        broken = [
            {"id": 1},
            {"id": 2, "operationAmount": None},
            {"id": 3, "operationAmount": {"currency": None}},
        ]
        assert list(filter_by_currency(broken, "USD")) == []


class TestFilterByCurrencyLaziness:
    """Проверка ленивости генератора."""

    def test_lazy_evaluation(self) -> None:
        """Функция не должна обходить весь список, если её не итерируют."""
        calls = {"count": 0}

        class CountingList(list):
            def __iter__(self):
                calls["count"] += 1
                return super().__iter__()

        data = CountingList([
            {"operationAmount": {"currency": {"code": "USD"}}},
            {"operationAmount": {"currency": {"code": "USD"}}},
        ])

        # создаём итератор, но не вызываем next() — обхода быть не должно
        _ = filter_by_currency(data, "USD")
        # вызываем один раз — должна быть только одна итерация
        next(_)
        # функция-генератор не перебирает всё сразу
        assert calls["count"] <= 1
