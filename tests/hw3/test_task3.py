from typing import Any, Dict, List

import pytest

from hw3.task3.hw3 import make_filter

sample_data = [
    {
        "name": "Bill",
        "last_name": "Gilbert",
        "occupation": "was here",
        "type": "person",
    },
    {
        "name": "Smudge",
        "type": "the Cat",
        "preferences": "he no like vegetals",
    },
    {
        "is_dead": True,
        "kind": "parrot",
        "name": "polly",
        "type": "bird",
    },
]


@pytest.mark.parametrize(
    "params, data, expected_result ",
    [
        ({"name": "404", "type": "error"}, sample_data, []),
        ({"name": "Bill", "occupation": "was here"}, sample_data, [sample_data[0]]),
        ({"name": "Smudge", "type": "the Cat"}, sample_data, [sample_data[1]]),
        ({"name": "polly", "type": "bird"}, sample_data, [sample_data[2]]),
    ],
)
def test_make_filter(
    params: Dict[Any, Any], data: List[Any], expected_result: List[Any]
):
    assert make_filter(**params).apply(data) == expected_result
