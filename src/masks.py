def get_mask_card_number(card_number: str) -> str:
    """Принимает номер карты и возвращает его маску в формате XXXX XX** **** XXXX."""
    card_number = card_number.replace(" ", "")

    # Выделяем нужные части номера
    first_four = card_number[:4]
    next_two = card_number[4:6]
    last_four = card_number[-4:]

    return f"{first_four} {next_two}** **** {last_four}"


def get_mask_account(account_number: str) -> str:
    """Принимает номер счета и возвращает его маску в формате **XXXX."""
    return f"**{account_number[-4:]}"
