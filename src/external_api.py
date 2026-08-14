import os

import requests
from dotenv import load_dotenv

load_dotenv()  # pragma: no cover
api_key = os.getenv("API_KEY")  # pragma: no cover


def convert_to_rubles(transaction: dict) -> float:
    """Функция принимает на вход транзакцию и возвращает сумму транзакции в рублях"""
    amount = transaction["operationAmount"]["amount"]
    if (
        transaction["operationAmount"]["currency"]["code"] == "USD"
        or transaction["operationAmount"]["currency"]["code"] == "EUR"
    ):
        url = "https://api.apilayer.com/exchangerates_data/latest"
        headers = {"apikey": api_key}

        response = requests.get(url, headers=headers)
        data = response.json()
        transfer_to_rubles = float(amount * data["rates"]["RUB"])
        return transfer_to_rubles
    return float(amount)
