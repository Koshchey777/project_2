import os

import pytest

from src.decorators import log


def test_log():
    @log(filename=None)
    def my_function(x, y):
        return x + y

    result = my_function(1, 2)
    assert result == "my_function ok, result: 3"


def test_log_error():
    @log(filename=None)
    def my_func(x, y):
        return x**y

    result = my_func("1", 2)
    assert (
        result == "my_func error: unsupported operand type(s) for ** or pow(): 'str' and 'int'. Inputs: ('1', 2), {}"
    )


def test_log_capsys(capsys):
    @log(filename=None)
    def hello_world():
        return "Hello, world!"

    print(hello_world())
    captured = capsys.readouterr()
    assert captured.out == "hello_world ok, result: Hello, world!\n"


def test_log_writes_to_file(tmp_path):
    log_file = tmp_path / "my_log.txt"

    @log(filename=str(log_file))
    def my_function(x, y):
        return x + y

    result = my_function(10, 20)
    assert result == "my_function ok, result: 30"
    assert log_file.exists()
    content = log_file.read_text(encoding="utf-8")
    assert "my_function ok, result: 30\n" in content


def test_log_kwargs():
    @log(filename=None)
    def age_name(age, name="User"):
        return f"{name}, youre {age} years old"

    result = age_name(10)
    assert result == "age_name ok, result: User, youre 10 years old"


def test_log_preserves_function_name():
    @log(filename=None)
    def secret_operation():
        pass

    assert secret_operation.__name__ == "secret_operation"


def test_log_catches_any_exception():
    @log(filename=None)
    def divide(a, b):
        return a / b

    result = divide(1, 0)

    assert "divide error: division by zero. Inputs: (1, 0), {}" in result


def test_log_handles_unicode(tmp_path):
    log_file = tmp_path / "unicode_log.txt"

    @log(filename=str(log_file))
    def say_hello():
        return "Привет 🌍"

    result = say_hello()
    assert result == "say_hello ok, result: Привет 🌍"
    content = log_file.read_text(encoding="utf-8")
    assert "say_hello ok, result: Привет 🌍\n" in content


def test_log_appends_multiple_calls(tmp_path):
    log_file = tmp_path / "multi_log.txt"

    @log(filename=str(log_file))
    def counter(x):
        return x + 1

    result1 = counter(1)
    result2 = counter(2)
    result3 = counter(3)

    assert result1 == "counter ok, result: 2"
    assert result2 == "counter ok, result: 3"
    assert result3 == "counter ok, result: 4"

    lines = log_file.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 3

    # Проверяем, что все сообщения присутствуют
    assert "counter ok, result: 2" in lines
    assert "counter ok, result: 3" in lines
    assert "counter ok, result: 4" in lines


def test_log_handles_file_write_error(tmp_path):
    log_file = tmp_path / "locked.log"

    log_file.write_text("dummy content")
    if os.name == "nt":  # Windows
        import stat

        os.chmod(log_file, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
        os.chmod(log_file, 0o444)

    @log(filename=str(log_file))
    def safe_function(x):
        return x * 2

    result = safe_function(10)

    assert result == "safe_function ok, result: 20"

    content = log_file.read_text(encoding="utf-8")
    assert content == "dummy content"
