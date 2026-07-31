def filter_by_currency(transactions: list, currency: str):
    """Функция возвращает итератор, который поочередно выдает транзакции,
    где валюта операции соответствует заданной"""
    result = (x for x in transactions if x["operationAmount"]["currency"]["name"] == currency)
    return result


def transaction_descriptions(transactions_: list):
    """Генератор, который принимает список словарей с транзакциями
    и возвращает описание каждой операции по очереди"""
    for transaction in transactions_:
        if transaction["description"]:
            yield transaction["description"]


def card_number_generator(start: int, stop: int):
    """Генератор, который выдает номера банковских карт в формате
    XXXX XXXX XXXX XXXX, где X — цифра номера карты"""
    if 1 <= start <= 9999999999999999 and 1 <= stop <= 9999999999999999 and start <= stop:
        for n in range(int(start), int(stop) + 1):
            count_zero = 16 - len(str(n))
            result = "0" * count_zero + str(n)
            yield f"{result[:4]} {result[4:8]} {result[8:12]} {result[12:]}"
    else:
        yield ("Генератор может сгенерировать номера карт в заданном диапазоне от "
               "0000 0000 0000 0001 до 9999 9999 9999 9999.")
