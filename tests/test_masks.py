import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize(
    "card_input, result",
    [
        ("7000792289606361", "7000 79** **** 6361"),
        ("700079228960636155", "Неправильно введен номер карты. Попробуйте еще раз."),
        ("70007922896063", "Неправильно введен номер карты. Попробуйте еще раз."),
        ("", "Неправильно введен номер карты. Попробуйте еще раз."),
    ],
)
def test_get_mask_card_number(card_input, result):
    assert get_mask_card_number(card_input) == result


@pytest.mark.parametrize(
    "account_number, result",
    [
        ("73654108430135874305", "**4305"),
        ("4108430135874305", "**4305"),
        ("736541084301312525874305", "**4305"),
        ("123", "Неправильно введен номер счета. Попробуйте еще раз."),
    ],
)
def test_get_mask_account(account_number, result):
    assert get_mask_account(account_number) == result
