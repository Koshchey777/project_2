import logging
import os

logger_masks = logging.getLogger(__name__)
base_dir = os.path.dirname(os.path.dirname(__file__))
log_path = os.path.join(base_dir, "logs", "application_masks.log")
masks_handler = logging.FileHandler(log_path, mode="w")
masks_formatter = logging.Formatter("%(asctime)s: %(filename)s - %(levelname)s - %(message)s")
masks_handler.setFormatter(masks_formatter)
logger_masks.addHandler(masks_handler)
logger_masks.setLevel(logging.DEBUG)


def get_mask_card_number(card_input: str) -> str:
    """Функция маскировки номера банковской карты"""
    if len(card_input) == 16:
        hidden_card = card_input[:4] + " " + card_input[4:6] + "** **** " + card_input[12:]
        logger_masks.info("Маскировка номера банковской карты прошла успешно")
        return hidden_card
    else:
        logger_masks.error("Неверный ввод номера карты")
        return "Неправильно введен номер карты. Попробуйте еще раз."


def get_mask_account(account_number: str) -> str:
    """Функция маскировки номера банковского счета"""
    if len(account_number) >= 4:
        hidden_account_number = "**" + account_number[-4:]
        logger_masks.info("Маскировка номера банковского счета прошла успешно")
        return hidden_account_number
    else:
        logger_masks.error("Неверный ввод номера счета")
        return "Неправильно введен номер счета. Попробуйте еще раз."
