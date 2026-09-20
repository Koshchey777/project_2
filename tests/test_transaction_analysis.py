from src.transaction_analysis import process_bank_operations, process_bank_search


def test_search_finds_one_match():
    data = [
        {"id": 1, "description": "Оплата в Пятерочке"},
        {"id": 2, "description": "Перевод другу"},
    ]
    result = process_bank_search(data, "Пятероч")
    assert len(result) == 1
    assert result[0]["id"] == 1


def test_search_finds_multiple_matches():
    data = [
        {"id": 1, "description": "Оплата в Пятерочке"},
        {"id": 2, "description": "Перевод другу"},
        {"id": 3, "description": "Возврат в Пятерочке"},
    ]
    result = process_bank_search(data, "Пятероч")
    assert len(result) == 2
    assert {r["id"] for r in result} == {1, 3}


def test_search_case_insensitive():
    data = [
        {"id": 1, "description": "ОПЛАТА В МАГАЗИНЕ ПЯТЕРОЧКА"},
    ]
    result = process_bank_search(data, "пятерочка")
    assert len(result) == 1


def test_search_no_match():
    data = [
        {"id": 1, "description": "Оплата в Магните"},
    ]
    result = process_bank_search(data, "Пятерочка")
    assert result == []


def test_search_empty_data():
    assert process_bank_search([], "тест") == []


def test_search_non_string_description_skipped():
    data = [
        {"id": 1, "description": 12345},
        {"id": 2, "description": "Оплата в Пятерочке"},
    ]
    result = process_bank_search(data, "Пятероч")
    assert len(result) == 1
    assert result[0]["id"] == 2


def test_search_partial_substring():
    data = [
        {"id": 1, "description": "Супермаркет Пятёрочка у дома"},
    ]
    result = process_bank_search(data, "маркет")
    assert len(result) == 1


def test_operations_basic_count():
    data = [
        {"description": "Продукты"},
        {"description": "Транспорт"},
        {"description": "Продукты"},
    ]
    categories = ["Продукты", "Транспорт", "Рестораны"]
    result = process_bank_operations(data, categories)
    assert result["Продукты"] == 2
    assert result["Транспорт"] == 1
    assert "Рестораны" not in result


def test_operations_no_match():
    data = [
        {"description": "Аптека"},
        {"description": "Одежда"},
    ]
    categories = ["Продукты", "Транспорт"]
    result = process_bank_operations(data, categories)
    assert result == {}


def test_operations_empty_data():
    result = process_bank_operations([], ["Продукты"])
    assert result == {}


def test_operations_empty_categories():
    data = [
        {"description": "Продукты"},
    ]
    result = process_bank_operations(data, [])
    assert result == {}


def test_operations_case_sensitive():
    data = [
        {"description": "продукты"},
        {"description": "Продукты"},
    ]
    categories = ["Продукты"]
    result = process_bank_operations(data, categories)
    assert result["Продукты"] == 1


def test_operations_all_same_category():
    data = [
        {"description": "Продукты"},
        {"description": "Продукты"},
        {"description": "Продукты"},
    ]
    result = process_bank_operations(data, ["Продукты"])
    assert result["Продукты"] == 3


def test_operations_returns_counter_type():
    from collections import Counter

    data = [{"description": "Продукты"}]
    result = process_bank_operations(data, ["Продукты"])
    assert isinstance(result, Counter)


def test_operations_duplicate_in_categories():
    data = [
        {"description": "Продукты"},
        {"description": "Продукты"},
    ]
    categories = ["Продукты", "Продукты"]
    result = process_bank_operations(data, categories)
    assert result["Продукты"] == 4
