import pytest
from src.generators import filter_by_currency, transaction_descriptions, card_number_generator

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


@pytest.fixture
def coll_transactions():
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "RUB", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
    ]


@pytest.fixture
def wrong_transactions():
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "descrition": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "RUB", "code": "USD"}},
            "descrition": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
    ]


def test_filter_by_currency(coll_transactions):
    usd_transactions = filter_by_currency(coll_transactions, "USD")
    rub_transactions = filter_by_currency(coll_transactions, "RUB")
    assert next(usd_transactions) == {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702",
    }
    assert next(rub_transactions) == {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {"amount": "79114.93", "currency": {"name": "RUB", "code": "USD"}},
        "description": "Перевод со счета на счет",
        "from": "Счет 19708645243227258542",
        "to": "Счет 75651667383060284188",
    }


def test_filter_by_currency_wrong_data(coll_transactions):
    wrong_transactions = filter_by_currency(coll_transactions, "RU")
    empty_list = filter_by_currency([], "RU")
    with pytest.raises(StopIteration):
        next(wrong_transactions)

    with pytest.raises(StopIteration):
        next(empty_list)


@pytest.mark.parametrize(
    "transactions, result",
    [
        (
            [
                {
                    "id": 939719570,
                    "state": "EXECUTED",
                    "date": "2018-06-30T02:08:58.425572",
                    "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
                    "description": "Перевод организации",
                    "from": "Счет 75106830613657916952",
                    "to": "Счет 11776614605963066702",
                },
                {
                    "id": 142264268,
                    "state": "EXECUTED",
                    "date": "2019-04-04T23:20:05.206878",
                    "operationAmount": {"amount": "79114.93", "currency": {"name": "RUB", "code": "USD"}},
                    "description": "Перевод со счета на счет",
                    "from": "Счет 19708645243227258542",
                    "to": "Счет 75651667383060284188",
                },
            ],
            ["Перевод организации", "Перевод со счета на счет"],
        )
    ],
)
def test_transaction_descriptions(transactions, result):
    descriptions = list(transaction_descriptions(transactions))
    assert descriptions == result


def test_transaction_descriptions_wrong(wrong_transactions):
    gen = transaction_descriptions(wrong_transactions)
    with pytest.raises(KeyError):
        next(gen)


def test_transaction_descriptions_empty_list():
    with pytest.raises(StopIteration):
        descriptions = transaction_descriptions([])
        next(descriptions)


@pytest.mark.parametrize(
    "start, stop, result",
    [
        (
            1,
            5,
            [
                "0000 0000 0000 0001",
                "0000 0000 0000 0002",
                "0000 0000 0000 0003",
                "0000 0000 0000 0004",
                "0000 0000 0000 0005",
            ],
        ),
        (9999999999999998, 9999999999999999, ["9999 9999 9999 9998", "9999 9999 9999 9999"]),
    ],
)
def test_card_number_generator(start, stop, result):
    card_number = list(card_number_generator(start, stop))
    assert card_number == result


def test_card_number_generator_wrong_range():
    card_number_1 = list(card_number_generator(0, 5))
    card_number_2 = list(card_number_generator(9999999999999999, 99999999999999999))
    assert card_number_1 == [
        "Генератор может сгенерировать номера карт в заданном диапазоне от 0000 0000 0000 0001 до 9999 9999 9999 9999."
    ]
    assert card_number_2 == [
        "Генератор может сгенерировать номера карт в заданном диапазоне от 0000 0000 0000 0001 до 9999 9999 9999 9999."
    ]
