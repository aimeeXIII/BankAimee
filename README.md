# Проект "Банковский виджет и обработка данных"

## Описание проекта
Этот проект представляет собой наборутилитарных модулей на Python для обработки и фильтрации банковских данных (транзакций), маскирования конфиденциальной информации (номеров карт и счетов) и форматирования дат. Он закладывает основу для логики личного кабинета пользователя.

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com
   cd название_репозитория
   ```

2. Убедитесь, что у вас установлен Python версии 3.10 или выше.

3. (Опционально) Установите зависимости для тестирования:
   ```bash
   pip install pytest
   ```

## Использование модулей и функций

### 1. Модуль `masks`
Содержит базовые функции скрытия персональных данных.

* **`get_mask_card_number(card_number)`**: Маскирует номер карты. Возвращает строку в формате `XXXX XX** **** XXXX`.
* **`get_mask_account(account_number)`**: Маскирует номер счета. Возвращает последние 4 цифры в формате `**XXXX`.

### 2. Модуль `widget`
Содержит высокоуровневые функции для подготовки данных к отображению в интерфейсе.

* **`mask_account_card(info_string)`**: Автоматически определяет тип платежного средства (карта или счет) и маскирует номер, сохраняя текстовое название.
* **`get_date(date_string)`**: Преобразует строку даты из формата ISO (например, `"2024-03-11T02:26:18"`) в привычный формат `"ДД.ММ.ГГГГ"`.

**Примеры работы:**
```python
from src.widget import get_date, mask_account_card

# Маскирование карты
print(mask_account_card("Visa Platinum 7000792289606361"))  
# Вывод: Visa Platinum 7000 79** **** 6361

# Маскирование счета
print(mask_account_card("Счет 73654108430135874305"))  
# Вывод: Счет **4305

# Форматирование даты
print(get_date("2024-03-11T02:26:18.671407"))  
# Вывод: 11.03.2024
```

### 3. Модуль `processing`
Предоставляет инструменты для аналитики и фильтрации списков транзакций.

* **`filter_by_state(data, state_value)`**: Фильтрует список словарей по статусу операции (`'EXECUTED'` по умолчанию).
* **`sort_by_date(data, reverse)`**: Сортирует список словарей по дате операции (по умолчанию — от самых свежих к самым старым).

**Примеры работы:**
```python
from src.processing import filter_by_state, sort_by_date

transactions = [
    {'id': 1, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58'},
    {'id': 2, 'state': 'CANCELED', 'date': '2019-07-03T18:35:29'},
]

# Фильтрация только выполненных транзакций
print(filter_by_state(transactions)) 

# Сортировка транзакций по дате
print(sort_by_date(transactions, reverse=True))
```
### 4. Модуль `generators`

Содержит функции-генераторы для ленивой обработки транзакций и создания тестовых данных.

* **`filter_by_currency(transactions, currency_code)`**: Возвращает итератор по транзакциям, у которых код валюты совпадает с заданным (например, `"USD"`).
* **`transaction_descriptions(transactions)`**: Возвращает описания операций по очереди.
* **`card_number_generator(start, end)`**: Генерирует номера карт в формате `XXXX XXXX XXXX XXXX` в заданном диапазоне.

**Примеры работы:**

```python
from generators.filter_by_currency import filter_by_currency
from generators.transaction_descriptions import transaction_descriptions
from generators.card_number_generator import card_number_generator
transactions = [
    {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {
            "amount": "9824.07",
            "currency": {"name": "USD", "code": "USD"},
        },
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702",
    },
    {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {
            "amount": "79114.93",
            "currency": {"name": "USD", "code": "USD"},
        },
        "description": "Перевод со счета на счет",
        "from": "Счет 19708645243227258542",
        "to": "Счет 75651667383060284188",
    },
    {
        "id": 873106923,
        "state": "EXECUTED",
        "date": "2019-03-23T01:09:46.296404",
        "operationAmount": {
            "amount": "43318.34",
            "currency": {"name": "руб.", "code": "RUB"},
        },
        "description": "Перевод со счета на счет",
        "from": "Счет 44812258784861134719",
        "to": "Счет 74489636417521191160",
    },
    {
        "id": 895315941,
        "state": "EXECUTED",
        "date": "2018-08-19T04:27:37.904916",
        "operationAmount": {
            "amount": "56883.54",
            "currency": {"name": "USD", "code": "USD"},
        },
        "description": "Перевод с карты на карту",
        "from": "Visa Classic 6831982476737658",
        "to": "Visa Platinum 8990922113665229",
    },
    {
        "id": 594226727,
        "state": "CANCELED",
        "date": "2018-09-12T21:27:25.241689",
        "operationAmount": {
            "amount": "67314.70",
            "currency": {"name": "руб.", "code": "RUB"},
        },
        "description": "Перевод организации",
        "from": "Visa Platinum 1246377376343588",
        "to": "Счет 14211924144426031657",
    },
]

# 1. Фильтрация транзакций по валюте
usd_transactions = filter_by_currency(transactions, "USD")
for _ in range(2):
    print(next(usd_transactions))
# Вывод:
# {'id': 939719570, ..., 'description': 'Перевод организации', ...}
# {'id': 142264268, ..., 'description': 'Перевод со счета на счет', ...}

# 2. Описания операций по очереди
descriptions = transaction_descriptions(transactions)
for _ in range(5):
    print(next(descriptions))
# Вывод:
# Перевод организации
# Перевод со счета на счет
# Перевод со счета на счет
# Перевод с карты на карту
# Перевод организации

# 3. Генерация номеров карт
for card_number in card_number_generator(1, 5):
    print(card_number)
# Вывод:
# 0000 0000 0000 0001
# 0000 0000 0000 0002
# 0000 0000 0000 0003
# 0000 0000 0000 0004
# 0000 0000 0000 0005
```

## Тестирование
Для запуска автоматических тестов выполните в корне проекта команду:
```bash
pytest
```
