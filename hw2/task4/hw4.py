"""
Write a function that accepts another function as an argument. Then it
should return such a function, so the every call to initial one
should be cached.


def func(a, b):
    return (a ** b) ** 2


cache_func = cache(func)

some = 100, 200

val_1 = cache_func(*some)
val_2 = cache_func(*some)

assert val_1 is val_2

"""
from typing import Any, Callable, Sequence


def cache(func: Callable) -> Callable:
    # use memoization technique
    memoization = {}

    def wrapper(*args: Sequence[Any]) -> Any:
        if args in memoization:
            return memoization[args]
        else:
            res = memoization[args] = func(*args)
            return res

    return wrapper
