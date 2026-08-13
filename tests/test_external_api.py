from unittest.mock import Mock, patch

import pytest

from src.external_api import convert_to_rubles


@pytest.fixture
def coll_transactions():
    return {"amount": 100.0, "currency": "USD"}


@patch("src.external_api.requests.get")
def test_convert_to_rubles(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {"rates": {"RUB": 90.5}}
    mock_get.return_value = mock_response

    transaction = {"amount": 100.0, "currency": "USD"}

    assert convert_to_rubles(transaction) == 9050.0
    mock_get.assert_called_once()


@pytest.fixture
def coll_transactions_():
    return {"amount": 100.0, "currency": "RUB"}


def test_convert_to_rubles_not_usd_eur(coll_transactions_):
    result = convert_to_rubles(coll_transactions_)
    assert result == 100.0
