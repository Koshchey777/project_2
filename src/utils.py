import json


def load_transactions(transaction_file) -> list:
    """Функция принимает на вход путь до JSON-файла и возвращает
    список словарей с данными о финансовых транзакциях"""
    try:
        with open(transaction_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
    except (json.JSONDecodeError, FileNotFoundError):
        return []
