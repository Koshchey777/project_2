import re
from collections import Counter


def process_bank_search(data: list[dict], search_str: str) -> list[dict]:
    """Функция возвращает список словарей, у которых в описании есть задаваемая строка"""
    result = []
    pattern = re.compile(rf"{search_str}", re.IGNORECASE)
    for i in data:
        if isinstance(i["description"], str) and pattern.search(i["description"]):
            result.append(i)
    return result


def process_bank_operations(data: list[dict], categories: list) -> dict:
    """Функция возвращает словарь, в котором ключи — это названия категорий,
    а значения — это количество операций в каждой категории."""
    list_categories = []
    for operation in data:
        for category in categories:
            if operation["description"] == category:
                list_categories.append(operation["description"])
    result = Counter(list_categories)
    return result
