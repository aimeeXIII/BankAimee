import logging
import os

# Создаем папку logs, если её нет
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)


def get_logger(name: str) -> logging.Logger:
    """Создает и настраивает логгер для указанного модуля.

    Логи пишутся в файл logs/<name>.log с перезаписью при каждом запуске.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Если у логгера уже есть обработчики, не добавляем новые (чтобы избежать дублей)
    if logger.handlers:
        return logger

    # Настройка файла
    log_file = os.path.join(LOG_DIR, f"{name}.log")

    # mode="w" обеспечивает перезапись файла при каждом запуске
    file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")

    # Формат: время - имя модуля - уровень - сообщение
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
