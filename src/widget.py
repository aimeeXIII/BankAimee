from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(info_string: str) -> str:
    """Принимает строку с типом и номером карты/счета и возвращает строку с замаскированным номером."""
    parts = info_string.split()

    # Извлекаем номер (последний элемент) и название (все элементы до него)
    number = parts[-1]
    name = " ".join(parts[:-1])

    # Проверяем тип и применяем ваши функции маскировки
    if name.lower() == "счет":
        masked_number = get_mask_account(number)
    else:
        masked_number = get_mask_card_number(number)

    return f"{name} {masked_number}"

def get_date(date_string: str) -> str:
    """Принимает строку с датой в формате ISO и возвращает дату в формате ДД.ММ.ГГГГ."""
    # Извлекаем год, месяц и день с помощью срезов
    year = date_string[:4]
    month = date_string[5:7]
    day = date_string[8:10]

    # Собираем в нужном формате
    return f"{day}.{month}.{year}"
