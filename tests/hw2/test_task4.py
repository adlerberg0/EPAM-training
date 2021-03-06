from typing import Callable, Tuple

import pytest

from hw2.task4.keep_result import cache


@pytest.mark.parametrize(
    ["func", "args"],
    [
        (lambda a, b: (a ** b) ** 2, (100, 200)),
        (lambda a, b: (a ** b) ** 2, (0, 0)),
        (lambda a, b: (a ** b), (-10, 10)),
    ],
)
def test_task4(func: Callable, args: Tuple[int]):
    cache_func = cache(func)
    val_1 = cache_func(*args)
    val_2 = cache_func(*args)

    assert val_1 is val_2
