from src.logger_config import get_logger

logger = get_logger("masks")


def get_mask_card_number(card_number: str) -> str:
    """Принимает номер карты и возвращает его маску в формате XXXX XX** **** XXXX."""
    logger.info(f"Запрос маскировки карты. Входные данные: {card_number}")

    card_number = card_number.replace(" ", "")
    first_four = card_number[:4]
    next_two = card_number[4:6]
    last_four = card_number[-4:]

    result = f"{first_four} {next_two}** **** {last_four}"
    logger.info(f"Результат маскировки карты: {result}")

    return result


def get_mask_account(account_number: str) -> str:
    """Принимает номер счета и возвращает его маску в формате **XXXX."""
    logger.info(f"Запрос маскировки счета. Входные данные: {account_number}")

    result = f"**{account_number[-4:]}"
    logger.info(f"Результат маскировки счета: {result}")

    return result
