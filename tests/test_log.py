import pytest
from decorators.log import log


# ---------------------------------------------------------------------------
# Успешное выполнение — вывод в консоль
# ---------------------------------------------------------------------------

class TestLogSuccessConsole:
    """Логирование успеха в консоль (filename не передан)."""

    def test_success_message_in_console(self, capsys) -> None:
        @log()
        def add(x, y):
            return x + y

        add(1, 2)
        captured = capsys.readouterr()
        assert captured.out.strip() == "add ok"

    def test_returns_result(self) -> None:
        """Декоратор не ломает возвращаемое значение."""
        @log()
        def add(x, y):
            return x + y

        assert add(1, 2) == 3

    def test_preserves_name_and_docstring(self) -> None:
        """functools.wraps сохраняет __name__ и __doc__."""
        @log()
        def my_func(x):
            """Докстринг."""
            return x

        assert my_func.__name__ == "my_func"
        assert my_func.__doc__ == "Докстринг."


# ---------------------------------------------------------------------------
# Успешное выполнение — запись в файл
# ---------------------------------------------------------------------------

class TestLogSuccessFile:
    """Логирование успеха в файл."""

    def test_success_written_to_file(self, tmp_path) -> None:
        log_file = tmp_path / "mylog.txt"

        @log(filename=str(log_file))
        def add(x, y):
            return x + y

        add(1, 2)
        content = log_file.read_text(encoding="utf-8").strip()
        assert content == "add ok"

    def test_multiple_calls_append(self, tmp_path) -> None:
        """Повторные вызовы дописываются, а не перезаписывают файл."""
        log_file = tmp_path / "mylog.txt"

        @log(filename=str(log_file))
        def add(x, y):
            return x + y

        add(1, 2)
        add(3, 4)
        lines = log_file.read_text(encoding="utf-8").splitlines()
        assert lines == ["add ok", "add ok"]


# ---------------------------------------------------------------------------
# Ошибки
# ---------------------------------------------------------------------------

class TestLogError:
    """Логирование ошибок."""

    def test_error_message_in_console(self, capsys) -> None:
        @log()
        def broken(x, y):
            return x + y

        with pytest.raises(TypeError):
            broken(1, "a")

        captured = capsys.readouterr()
        assert "broken error: TypeError" in captured.out
        assert "Inputs: (1, 'a'), {}" in captured.out

    def test_error_is_reraised(self) -> None:
        """Декоратор не должен глотать исключение."""
        @log()
        def broken(x, y):
            raise ValueError("тест")

        with pytest.raises(ValueError):
            broken(1, 2)

    def test_error_written_to_file(self, tmp_path) -> None:
        log_file = tmp_path / "mylog.txt"

        @log(filename=str(log_file))
        def broken(x, y):
            return x + y

        with pytest.raises(TypeError):
            broken(1, "a")

        content = log_file.read_text(encoding="utf-8").strip()
        assert "broken error: TypeError" in content
        assert "Inputs: (1, 'a'), {}" in content

    @pytest.mark.parametrize(
        "a, b, error_type",
        [
            (1, "a", TypeError),
            ("a", 1, TypeError),
            (1, 0, ZeroDivisionError),
        ],
        ids=["int-plus-str", "str-plus-int", "divide-by-zero"],
    )
    def test_various_errors(self, capsys, a, b, error_type) -> None:
        @log()
        def op(x, y):
            if y == 0:
                return x / y
            return x + y

        with pytest.raises(error_type):
            op(a, b)

        captured = capsys.readouterr()
        assert f"op error: {error_type.__name__}" in captured.out


# ---------------------------------------------------------------------------
# Пример из задания
# ---------------------------------------------------------------------------

class TestExampleFromTask:
    """Точный сценарий из задания."""

    def test_example_success(self, tmp_path) -> None:
        log_file = tmp_path / "mylog.txt"

        @log(filename=str(log_file))
        def my_function(x, y):
            return x + y

        my_function(1, 2)

        assert log_file.read_text(encoding="utf-8").strip() == "my_function ok"
