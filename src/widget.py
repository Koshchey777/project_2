import re

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(type_and_number: str) -> str:
    """Функция для маскировки номера карты или счета"""
    number_mask = re.findall(r"\d+", type_and_number)

    if number_mask and len(number_mask[0]) == 16:
        return type_and_number.replace(number_mask[0], get_mask_card_number(number_mask[0]))
    elif number_mask and len(number_mask[0]) == 20:
        return type_and_number.replace(number_mask[0], get_mask_account(number_mask[0]))
    else:
        return "Неправильно введены данные. Попробуйте еще раз"


def get_date(date: str) -> str:
    """Преобразование даты в формат ДД.ММ.ГГГГ"""
    return f"{date[8:10]}.{date[5:7]}.{date[:4]}"
