from datetime import datetime

from src.widget import get_date

DATE_FORMAT = "%d.%m.%Y"


def filter_by_state(new_list: list, state: str = "EXECUTED") -> list:
    """Функция возвращает новый список словарей, содержащий только те словари,
    у которых ключ state соответствует указанному значению"""
    result = []
    for dictionary in new_list:
        if dictionary["state"] == state:
            result.append(dictionary)
    return result


def sort_by_date(new_list: list, reverse_order: bool = True) -> list:
    """Функция возвращает новый список, отсортированный по дате"""
    return sorted(new_list, key=lambda x: datetime.strptime(get_date(x["date"]), DATE_FORMAT), reverse=reverse_order)
