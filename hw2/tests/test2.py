from typing import Any, List, Tuple

import pytest
from task2.hw2 import major_and_minor_elem


@pytest.mark.parametrize(
    ["value", "expected_result"],
    [
        ([3, 2, 3], (3, 2)),
        ([2, 2, 1, 1, 1, 2, 2], (2, 1)),
        ([2, 2, 2, 2, 2, 2, 2], (2, 2)),
        ([-1, 2, -1, -1, -1, 2, 2, 2], (-1, -1)),
        ([2, -1, -1, -1, -1, 2, 2, 2], (2, 2)),
    ],
)
def test_task2(value: List[int], expected_result: Tuple[Any]):
    actual_result = major_and_minor_elem(value)

    assert actual_result == expected_result
