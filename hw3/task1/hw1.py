from typing import Any, Callable, Sequence


def cache(times: int) -> Callable:
    # use memoization technique
    def cache_dec(func: Callable):
        memoization = {}

        def wrapper(*args: Sequence[Any]) -> Any:
            if args in memoization and memoization[args][1] > 0:
                memoization[args][1] -= 1
                return memoization[args][0]
            else:
                memoization[args] = [func(*args), times]
                return memoization[args][0]

        return wrapper

    return cache_dec
