import unittest
from unittest.mock import mock_open, patch

import pandas as pd

from src.data_read import reader_csv, reader_xlsx

CSV_DATA = """id;state;date;amount;currency_name;currency_code;from;to;description
650703;EXECUTED;2023-09-05T11:30:32Z;16210;Sol;PEN;Счет 58803664561298323391;Счет 39745660563456619397;Перевод организации
3598919;EXECUTED;2020-12-06T23:00:58Z;29740;Peso;COP;Discover 3172601889670065;Discover 0720428384694643;Перевод с карты на карту
5380041;CANCELED;2021-02-01T11:54:58Z;23789;Peso;UYU;;Счет 23294994494356835683;Открытие вклада"""


class TestReaderCSV(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data=CSV_DATA)
    def test_returns_list_of_dicts(self, mock_file):
        """Функция возвращает список словарей"""
        result = reader_csv("fake/path.csv")

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 3)
        for row in result:
            self.assertIsInstance(row, dict)

    @patch("builtins.open", new_callable=mock_open, read_data=CSV_DATA)
    def test_first_row_fields(self, mock_file):
        """Проверка значений первой строки"""
        result = reader_csv("fake/path.csv")
        first = result[0]

        self.assertEqual(first["id"], "650703")
        self.assertEqual(first["state"], "EXECUTED")
        self.assertEqual(first["amount"], "16210")
        self.assertEqual(first["currency_code"], "PEN")
        self.assertEqual(first["description"], "Перевод организации")

    @patch("builtins.open", new_callable=mock_open, read_data=CSV_DATA)
    def test_empty_from_field(self, mock_file):
        """Пустое поле from остаётся пустой строкой, а не None"""
        result = reader_csv("fake/path.csv")
        third = result[2]

        self.assertEqual(third["from"], "")
        self.assertEqual(third["state"], "CANCELED")

    @patch("builtins.open", new_callable=mock_open, read_data=CSV_DATA)
    def test_open_called_with_correct_args(self, mock_file):
        """open вызван с правильным путём и параметрами"""
        reader_csv("../data/transactions.csv")

        mock_file.assert_called_once_with("../data/transactions.csv", newline="", encoding="utf-8")

    @patch("builtins.open", new_callable=mock_open, read_data="")
    def test_empty_file(self, mock_file):
        """Пустой файл"""
        result = reader_csv("empty.csv")
        self.assertEqual(result, [])


XLSX_DICT = {
    "id": [650703, 3598919],
    "state": ["EXECUTED", "EXECUTED"],
    "date": ["2023-09-05T11:30:32Z", "2020-12-06T23:00:58Z"],
    "amount": [16210, 29740],
    "currency_name": ["Sol", "Peso"],
    "currency_code": ["PEN", "COP"],
    "from": ["Счет 58803664561298323391", "Discover 3172601889670065"],
    "to": ["Счет 39745660563456619397", "Discover 0720428384694643"],
    "description": ["Перевод организации", "Перевод с карты на карту"],
}


class TestReaderXLSX(unittest.TestCase):

    @patch("pandas.read_excel")
    def test_returns_list_of_dicts(self, mock_read):
        """Функция возвращает список словарей"""
        data = {"id": [101, 102], "state": ["OK", "FAIL"], "amount": [100.5, 200.0]}
        mock_df = pd.DataFrame(data)
        mock_read.return_value = mock_df

        result = reader_xlsx("fake/path.xlsx")

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        for row in result:
            self.assertIsInstance(row, dict)

    @patch("pandas.read_excel")
    def test_first_row_values(self, mock_read):
        """Проверка значений первой строки"""
        data = {"id": [650703, 3598919], "state": ["EXECUTED", "EXECUTED"], "currency_code": ["PEN", "COP"]}
        mock_df = pd.DataFrame(data)
        mock_read.return_value = mock_df

        result = reader_xlsx("fake/path.xlsx")
        first = result[0]

        self.assertEqual(first["id"], 650703)
        self.assertEqual(first["state"], "EXECUTED")
        self.assertEqual(first["currency_code"], "PEN")

    @patch("pandas.read_excel")
    def test_handles_nan_as_none(self, mock_read):
        """Пустые ячейки в Excel становятся None (или NaN, который при конвертации в dict часто остается float('nan'))"""
        import numpy as np

        data = {"id": [1], "from": [np.nan], "to": ["Счет 123"]}
        mock_df = pd.DataFrame(data)
        mock_read.return_value = mock_df

        result = reader_xlsx("fake/path.xlsx")
        row = result[0]

        self.assertTrue(pd.isna(row["from"]))
        self.assertEqual(row["to"], "Счет 123")

    @patch("pandas.read_excel")
    def test_called_with_engine(self, mock_read):
        """read_excel вызван с engine='openpyxl'"""
        mock_read.return_value = pd.DataFrame({"id": [1]})

        reader_xlsx("../data/transactions.xlsx")

        mock_read.assert_called_once_with("../data/transactions.xlsx", engine="openpyxl")

    @patch("pandas.read_excel")
    def test_empty_file_returns_empty_list(self, mock_read):
        """Если в файле нет данных (только заголовки или пусто) — возвращается пустой список"""
        mock_df = pd.DataFrame()
        mock_read.return_value = mock_df

        result = reader_xlsx("empty.xlsx")

        self.assertIsInstance(result, list)
        self.assertEqual(result, [])

    @patch("pandas.read_excel")
    def test_column_names_match_keys(self, mock_read):
        """Ключи в словарях соответствуют названиям колонок Excel"""
        data = {"user_id": [1], "balance": [1000], "active": [True]}
        mock_df = pd.DataFrame(data)
        mock_read.return_value = mock_df

        result = reader_xlsx("test.xlsx")
        row = result[0]

        self.assertIn("user_id", row)
        self.assertIn("balance", row)
        self.assertIn("active", row)


if __name__ == "__main__":
    unittest.main(verbosity=2)
