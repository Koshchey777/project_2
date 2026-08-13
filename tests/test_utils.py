from unittest.mock import patch

import pytest

from src.utils import load_transactions


@patch("json.load")
def test_load_transactions(mock_file):
    mock_file.return_value = [
        {
            "id": 441945886,
            "state": "EXECUTED",
            "date": "2019-08-26T10:50:58.294041",
            "operationAmount": {"amount": "31957.58", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод организации",
            "from": "Maestro 1596837868705199",
            "to": "Счет 64686473678894779589",
        }
    ]
    assert load_transactions(mock_file) == [
        {
            "id": 441945886,
            "state": "EXECUTED",
            "date": "2019-08-26T10:50:58.294041",
            "operationAmount": {"amount": "31957.58", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод организации",
            "from": "Maestro 1596837868705199",
            "to": "Счет 64686473678894779589",
        }
    ]


@pytest.fixture
def nonexistent_file_path():
    return "абсолютно_несуществующий_путь_12345.json"


def test_load_transactions_error(nonexistent_file_path):
    result = load_transactions(nonexistent_file_path)
    assert result == []


def test_load_transactions_invalid_json(tmp_path):
    file_path = tmp_path / "bad.json"
    file_path.write_text("not a json object")
    result = load_transactions(str(file_path))
    assert result == []
