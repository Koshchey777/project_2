from unittest.mock import Mock, patch
import pytest

from src.external_api import convert_to_rubles


@pytest.fixture
def usd_transaction():
    return {"operationAmount": {"amount": "100.0", "currency": {"code": "USD"}}}


@pytest.fixture
def eur_transaction():
    return {"operationAmount": {"amount": "50.0", "currency": {"code": "EUR"}}}


@pytest.fixture
def rub_transaction():
    return {"operationAmount": {"amount": "200.0", "currency": {"code": "RUB"}}}


@patch("src.external_api.requests.get")
def test_convert_to_rubles_usd(mock_get, usd_transaction):
    mock_response = Mock()
    mock_response.json.return_value = {"rates": {"RUB": 90.5}}
    mock_get.return_value = mock_response

    result = convert_to_rubles(usd_transaction)
    assert result == 9050.0


@patch("src.external_api.requests.get")
def test_convert_to_rubles_eur(mock_get, eur_transaction):
    mock_response = Mock()
    mock_response.json.return_value = {"rates": {"RUB": 100.0}}
    mock_get.return_value = mock_response

    result = convert_to_rubles(eur_transaction)
    assert result == 5000.0


def test_convert_to_rubles_rub(rub_transaction):
    result = convert_to_rubles(rub_transaction)
    assert result == 200.0


def test_convert_to_rubles_other_currency(rub_transaction):
    transaction = {"operationAmount": {"amount": "300.0", "currency": {"code": "JPY"}}}
    result = convert_to_rubles(transaction)
    assert result == 300.0
