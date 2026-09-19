from src.data_read import reader_csv, reader_xlsx
from src.generators import filter_by_currency
from src.processing import filter_by_state, sort_by_date
from src.transaction_analysis import process_bank_search
from src.utils import load_transactions
from src.widget import get_date, mask_account_card

if __name__ == "__main__":

    type_information = ""
    while type_information not in ["1", "2", "3"]:
        type_information = input("""Привет! Добро пожаловать в программу работы 
с банковскими транзакциями. 
Выберите необходимый пункт меню:
1. Получить информацию о транзакциях из JSON-файла
2. Получить информацию о транзакциях из CSV-файла
3. Получить информацию о транзакциях из XLSX-файла
        """)
        if type_information not in ["1", "2", "3"]:
            print("""Введите цифру от 1 до 3.\n""")
        if type_information == "1":
            print("Для обработки выбран JSON-файл.")
        if type_information == "2":
            print("Для обработки выбран CSV-файл.")
        if type_information == "3":
            print("Для обработки выбран XLSX-файл.")

    state = ""
    while state.upper() not in ["EXECUTED", "CANCELED", "PENDING"]:
        state = input("""Введите статус, по которому необходимо выполнить фильтрацию. 
Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING
    """)
        if state.upper() not in ["EXECUTED", "CANCELED", "PENDING"]:
            print(f'Статус операции "{state}" недоступен.')
    print(f'Операции отфильтрованы по статусу "{state.upper()}"')

    sort_date = input("Отсортировать операции по дате? Да/Нет\n")
    if sort_date.lower() == "да":
        sort_sequence = input("Отсортировать по возрастанию или по убыванию?\n")

    sort_rub = input("Выводить только рублевые транзакции? Да/Нет\n")

    sort_word = input("Отфильтровать список транзакций по определенному слову в описании? Слово/нет\n")

    print("Распечатываю итоговый список транзакций...")

    if type_information == "1":
        read_file = load_transactions("data/transactions.json")
    if type_information == "2":
        read_file = reader_csv("data/transactions.csv")
    if type_information == "3":
        read_file = reader_xlsx("data/transactions.xlsx")

    read_file = filter_by_state(read_file, state)

    if sort_date.lower() == "да":
        if sort_sequence.lower() == "по возрастанию":
            read_file = sort_by_date(read_file, False)
        if sort_sequence.lower() == "по убыванию":
            read_file = sort_by_date(read_file, True)
    if sort_rub == "да":
        read_file = list(filter_by_currency(read_file, "RU"))

    if sort_word != "нет":
        read_file = process_bank_search(read_file, sort_word)

    for transaction in read_file:
        date = get_date(transaction.get("date", ""))
        description = transaction.get("description", "")
        from_ = mask_account_card(transaction.get("from", ""))
        to = mask_account_card(transaction.get("to", ""))
        amount = transaction.get("amount", "")

        print(f"{date} {description}")
        print(f"{from_} -> {to}")
        print(f"Сумма: {amount}\n")
