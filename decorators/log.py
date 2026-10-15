"""Декоратор для логирования вызовов функций."""
import functools
from typing import Any, Callable


def log(filename: str | None = None) -> Callable:
    """Декоратор логирует начало/конец функции, её результат или ошибку.

    Args:
        filename: путь к файлу для логов. Если None — вывод в консоль.

    Returns:
        Декоратор, который оборачивает функцию.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                result = func(*args, **kwargs)
                message = f"{func.__name__} ok"
            except Exception as e:
                message = (
                    f"{func.__name__} error: {type(e).__name__}. "
                    f"Inputs: {args}, {kwargs}"
                )
                write_log(message, filename)
                raise
            else:
                write_log(message, filename)
                return result

        return wrapper

    return decorator


def write_log(message: str, filename: str | None) -> None:
    """Пишет сообщение в файл или в консоль.

    Args:
        message: текст лога.
        filename: путь к файлу. Если None — печать в консоль.
    """
    if filename is None:
        print(message)
    else:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(message + "\n")
