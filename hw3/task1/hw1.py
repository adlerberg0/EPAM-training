from typing import Any, Callable, Sequence


def cache(times: int) -> Callable:
    def cache_dec(func: Callable):
        times_remains = 0
        res = None

        def wrapper(*args: Sequence[Any]) -> Any:
            nonlocal times_remains, res
            if times_remains > 0:
                times_remains -= 1

                return res
            else:
                res = func(*args)
                times_remains = times

                return res

        return wrapper

    return cache_dec
