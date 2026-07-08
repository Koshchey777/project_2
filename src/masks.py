def get_mask_card_number(card_input: str) -> str:
    """Функция маскировки номера банковской карты"""
    if len(card_input) == 16:
        hidden_card = card_input[:4] + " " + card_input[4:6] + "** **** " + card_input[12:]
        return hidden_card
    else:
        return "Неправильно введен номер карты. Попробуйте еще раз."


def get_mask_account(account_number: str) -> str:
    """Функция маскировки номера банковского счета"""
    if len(account_number) >= 4:
        hidden_account_number = "**" + account_number[-4:]
        return hidden_account_number
    else:
        return "Неправильно введен номер счета. Попробуйте еще раз."
