import pytest

from hw3.task4.hw4 import is_armstrong


@pytest.mark.parametrize("value, result", [(153, True), (10, False)])
def test_cache(value: int, result: bool):
    assert is_armstrong(value) is result
