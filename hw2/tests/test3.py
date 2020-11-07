from typing import Any, Sequence

import pytest
from task3.hw3 import combinations


@pytest.mark.parametrize(
    ["value", "expected_result"],
    [
        ([[1, 2], [3, 4]], [[1, 3], [1, 4], [2, 3], [2, 4]]),
    ],
)
def test_task3(value: Sequence[int], expected_result: Sequence[Any]):
    actual_result = combinations(*value)

    assert actual_result == expected_result
