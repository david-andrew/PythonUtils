from functools import wraps

def once(func):
    cur_func = func
    noop = lambda *args, **kwargs: None
    @wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal cur_func
        result = cur_func(*args, **kwargs)
        cur_func = noop
        return result
    return wrapper


@once
def hi():
    print('hello world')


if __name__ == "__main__":
    hi()  # prints 'hello world'
    hi()  # does nothing
    hi()  # does nothing
