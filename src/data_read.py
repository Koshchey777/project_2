from csv import DictReader
import pandas as pd


def reader_csv(file_path):
    """Чтение файлов формата csv"""
    with open(file_path, newline="", encoding="utf-8") as file:
        reader = DictReader(file, delimiter=";")
        return list(reader)


def reader_xlsx(file_path):
    """Чтение файлов формата excel"""
    df = pd.read_excel(file_path, engine="openpyxl")
    return df.to_dict(orient='records')
