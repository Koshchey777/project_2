import json
import logging
import os

logger_utils = logging.getLogger(__name__)
base_dir = os.path.dirname(os.path.dirname(__file__))
log_path = os.path.join(base_dir, "logs", "application_utils.log")
utils_handler = logging.FileHandler(log_path, mode="w")
utils_formatter = logging.Formatter("%(asctime)s: %(filename)s - %(levelname)s - %(message)s")
utils_handler.setFormatter(utils_formatter)
logger_utils.addHandler(utils_handler)
logger_utils.setLevel(logging.DEBUG)


def load_transactions(transaction_file) -> list:
    """Функция принимает на вход путь до JSON-файла и возвращает
    список словарей с данными о финансовых транзакциях"""
    try:
        with open(transaction_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            logger_utils.info("Загрузка прошла успешно")
            return data

    except (json.JSONDecodeError, FileNotFoundError) as ex:
        logger_utils.error(f"При загрузке произошла ошибка: {ex}")
        return []
