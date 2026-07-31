import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "type_and_number, result",
    [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Счет 73654108430135874305", "Счет **4305"),
        ("Visa Platinum 700079228960636", "Неправильно введены данные. Попробуйте еще раз"),
        ("Счет 7365410843013545562874305", "Неправильно введены данные. Попробуйте еще раз"),
    ],
)
def test_mask_account_card(type_and_number, result):
    assert mask_account_card(type_and_number) == result


@pytest.mark.parametrize(
    "date, result",
    [("2024-03-11T02:26:18.671407", "11.03.2024"), ("2026-07-24T02:26:19.671407", "24.07.2026"), ("", "..")],
)
def test_get_date(date, result):
    assert get_date(date) == result


@pytest.mark.parametrize("date", [(202403112618671407), (202607242619671407)])
def test_get_date_wrong_type(date):
    with pytest.raises(TypeError):
        get_date(date)
