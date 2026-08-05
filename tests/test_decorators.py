import pytest
import os


from src.decorators import log

def test_log():
    @log(filename=None)
    def my_function(x, y):
        return x + y

    result = my_function(1, 2)
    assert result == 'my_function ok'

def test_log_error():
    @log(filename=None)
    def my_func(x, y):
        return x ** y

    result = my_func("1", 2)
    assert result == "my_func error: unsupported operand type(s) for ** or pow(): 'str' and 'int'. Inputs: ('1', 2), {}"

def test_log_capsys(capsys):
    @log(filename=None)
    def hello_world():
        return "Hello, world!"

    print(hello_world())
    captured = capsys.readouterr()
    assert captured.out == "hello_world ok\n"


def test_log_writes_to_file(tmp_path):
    log_file = tmp_path / "my_log.txt"

    @log(filename=str(log_file))
    def my_function(x, y):
        return x + y

    result = my_function(10, 20)

    assert result == "my_function ok"
    assert log_file.exists()
    content = log_file.read_text(encoding="utf-8")
    assert "my_function ok\n" in content

def test_log_kwargs():
    @log(filename=None)
    def age_name(age, name='User'):
        return f'{name}, youre {age} years old'

    result = age_name(10)
    assert result == 'age_name ok'


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

    assert "divide error" in result
    assert "ZeroDivisionError" in result or "division by zero" in result


def test_log_handles_unicode(tmp_path):
    log_file = tmp_path / "unicode_log.txt"

    @log(filename=str(log_file))
    def say_hello():
        return "Привет 🌍"

    say_hello()

    content = log_file.read_text(encoding="utf-8")
    assert "say_hello ok" in content


def test_log_appends_multiple_calls(tmp_path):
    log_file = tmp_path / "multi_log.txt"

    @log(filename=str(log_file))
    def counter(x):
        return x + 1

    counter(1)
    counter(2)
    counter(3)

    lines = log_file.read_text(encoding="utf-8").splitlines()

    assert len(lines) == 3
    assert all("counter ok" in line for line in lines)


