from functools import wraps


def log(filename=None):
    """Декоратор, который автоматически логирует начало и конец
    выполнения функции, а также ее результаты или возникшие ошибки"""

    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                res = f"{func.__name__} ok"
            except Exception as e:
                result = None
                res = f"{func.__name__} error: {e}. Inputs: {args}, {kwargs}"
            if filename is not None:
                with open(filename, "a", encoding="utf-8") as f:
                    f.write(res + "\n")
            return res

        return inner

    return wrapper
