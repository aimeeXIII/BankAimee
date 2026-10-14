import pytest
from generators.card_number_generator import card_number_generator


class TestCardNumberGenerator:
    """Тесты генератора номеров карт."""

    def test_returns_iterator(self) -> None:
        """Функция возвращает именно генератор-итератор."""
        result = card_number_generator(1, 3)
        assert hasattr(result, "__iter__")
        assert hasattr(result, "__next__")
        assert not isinstance(result, list)

    def test_example_from_task(self) -> None:
        """Кейс из задания: (1, 5)."""
        result = list(card_number_generator(1, 5))
        assert result == [
            "0000 0000 0000 0001",
            "0000 0000 0000 0002",
            "0000 0000 0000 0003",
            "0000 0000 0000 0004",
            "0000 0000 0000 0005",
        ]

    def test_next_yields_one_by_one(self) -> None:
        """next() поочерёдно выдаёт номера, потом StopIteration."""
        iterator = card_number_generator(1, 3)
        assert next(iterator) == "0000 0000 0000 0001"
        assert next(iterator) == "0000 0000 0000 0002"
        assert next(iterator) == "0000 0000 0000 0003"
        with pytest.raises(StopIteration):
            next(iterator)

    def test_format_has_16_digits(self) -> None:
        """Формат: 4 группы по 4 цифры, разделённые пробелами."""
        for number in card_number_generator(1, 100):
            parts = number.split(" ")
            assert len(parts) == 4
            assert all(len(part) == 4 and part.isdigit() for part in parts)

    def test_range_includes_both_ends(self) -> None:
        """Диапазон включает и start, и end."""
        result = list(card_number_generator(5, 7))
        assert result == [
            "0000 0000 0000 0005",
            "0000 0000 0000 0006",
            "0000 0000 0000 0007",
        ]

    def test_single_value_range(self) -> None:
        """start == end — одно значение."""
        assert list(card_number_generator(42, 42)) == ["0000 0000 0000 0042"]

    def test_empty_range(self) -> None:
        """start > end — пустой итератор."""
        assert list(card_number_generator(10, 5)) == []

    @pytest.mark.parametrize(
        "start, end, expected",
        [
            (1, 1, ["0000 0000 0000 0001"]),
            (0, 0, ["0000 0000 0000 0000"]),
            (9999, 9999, ["0000 0000 0000 9999"]),
            (1, 2, [
                "0000 0000 0000 0001",
                "0000 0000 0000 0002",
            ]),
        ],
        ids=["one", "zero", "big", "two"],
    )
    def test_parametrized(self, start: int, end: int, expected: list[str]) -> None:
        assert list(card_number_generator(start, end)) == expected

    def test_max_value_format(self) -> None:
        """Максимальное значение диапазона — 9999 9999 9999 9999."""
        result = list(card_number_generator(9999999999999999, 9999999999999999))
        assert result == ["9999 9999 9999 9999"]

    def test_lazy_evaluation(self) -> None:
        """Генератор не создаёт весь список сразу — только выдаёт по одному."""
        # если бы функция возвращала список, для range(1, 10**16) не хватило бы памяти
        # генератор создаётся мгновенно и первый next тоже
        iterator = card_number_generator(1, 9999999999999999)
        assert next(iterator) == "0000 0000 0000 0001"
        assert next(iterator) == "0000 0000 0000 0002"
        assert next(iterator) == "0000 0000 0000 0003"