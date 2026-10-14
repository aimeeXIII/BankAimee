from typing import Iterator


def card_number_generator(start: int, end: int) -> Iterator[str]:

    for number in range(start, end + 1):
        card_number = f"{number:016d}"
        yield f"{card_number[:4]} {card_number[4:8]} {card_number[8:12]} {card_number[12:]}"