from src.masks import get_mask_account, get_mask_card_number
from src.processing import filter_by_state, sort_by_date
from src.search import process_bank_search
from src.utils import load_transactions
from src.widget import get_date

STATUSES = ["EXECUTED", "CANCELED", "PENDING"]


def main() -> None:
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("Ваш выбор: ").strip()

    if choice == "1":
        print("Для обработки выбран JSON-файл.")
        file_path = "data/operations.json"
    elif choice == "2":
        print("Для обработки выбран CSV-файл.")
        file_path = "data/transactions.csv"
    elif choice == "3":
        print("Для обработки выбран XLSX-файл.")
        file_path = "data/transactions_excel.xlsx"
    else:
        print("Неверный пункт меню. Завершение программы.")
        return

    transactions = load_transactions(file_path)
    if not transactions:
        print("Не удалось загрузить данные. Проверьте файл.")
        return

    # --- Фильтрация по статусу ---
    print("Введите статус, по которому необходимо выполнить фильтрацию.")
    print(f"Доступные для фильтровки статусы: {', '.join(STATUSES)}")

    while True:
        status = input("Введите статус: ").strip().upper()
        if status in STATUSES:
            print(f'Операции отфильтрованы по статусу "{status}"')
            break
        print(f'Статус операции "{status}" недоступен.')

    filtered = filter_by_state(transactions, status)

    # --- Сортировка по дате ---
    sort_choice = input("Отсортировать операции по дате? Да/Нет: ").strip().lower()
    if sort_choice in ("да", "yes"):
        order = input("Отсортировать по возрастанию или по убыванию? ").strip().lower()
        reverse = order in ("по убыванию", "desc")
        filtered = sort_by_date(filtered, reverse=reverse)

    # --- Фильтрация по рублям ---
    rub_choice = input("Выводить только рублевые транзакции? Да/Нет: ").strip().lower()
    if rub_choice in ("да", "yes"):
        rub_transactions = []
        for t in filtered:
            try:
                if t["operationAmount"]["currency"]["code"] == "RUB":
                    rub_transactions.append(t)
            except (KeyError, TypeError):
                pass
        filtered = rub_transactions

    # --- Поиск по описанию ---
    search_choice = input(
        "Отфильтровать список транзакций по определенному слову в описании? Да/Нет: ").strip().lower()
    if search_choice in ("да", "yes"):
        search_word = input("Введите слово для поиска: ").strip()
        filtered = process_bank_search(filtered, search_word)

    # --- Вывод результата ---
    print("Распечатываю итоговый список транзакций...\n")

    if not filtered:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
        return

    print(f"Всего банковских операций в выборке: {len(filtered)}\n")

    for t in filtered:
        date = get_date(t.get("date", ""))
        desc = t.get("description", "")

        # Маскируем отправителя и получателя
        from_acc = t.get("from")
        to_acc = t.get("to")

        from_masked = ""
        if from_acc:
            if from_acc.startswith("Счет"):
                from_masked = f"Счет {get_mask_account(from_acc.split()[-1])}"
            else:
                name = " ".join(from_acc.split()[:-1])
                from_masked = f"{name} {get_mask_card_number(from_acc.split()[-1])}"

        to_masked = ""
        if to_acc:
            if to_acc.startswith("Счет"):
                to_masked = f"Счет {get_mask_account(to_acc.split()[-1])}"
            else:
                name = " ".join(to_acc.split()[:-1])
                to_masked = f"{name} {get_mask_card_number(to_acc.split()[-1])}"

        print(f"{date} {desc}")

        if from_masked and to_masked:
            print(f"{from_masked} -> {to_masked}")
        elif to_masked:
            print(f"{to_masked}")

        # Сумма
        amount = t.get("operationAmount", {}).get("amount", "")
        currency = t.get("operationAmount", {}).get("currency", {}).get("code", "")

        if currency == "RUB":
            print(f"Сумма: {amount} руб.\n")
        else:
            # Если нужна конвертация (необязательно для вывода, но можно)
            print(f"Сумма: {amount} {currency}\n")


if __name__ == "__main__":
    main()
