from typing import Any, Sequence

import pytest

from hw2.task1.deal_with_unicode import count_non_ascii_chars  # noqa
from hw2.task1.deal_with_unicode import count_punctuation_chars  # noqa
from hw2.task1.deal_with_unicode import get_longest_diverse_words  # noqa
from hw2.task1.deal_with_unicode import get_most_common_non_ascii_char  # noqa
from hw2.task1.deal_with_unicode import get_rarest_char  # noqa

tmp_set1 = {
    "résistance-Bewegungen,",
    "Schicksalsfiguren;",
    "Zwingherrschaft.",
    "unmißverständliche",
    "Kollektivschuldiger,",
    "Selbstverständlich",
    "Bevölkerungsabschub,",
    "Werkstättenlandschaft",
    "politisch-strategischen",
    "Machtbewußtsein,",
}
tmp_list2 = ["»", "«", "—", ",", ".", "-", "?", ";", ":", "›", "‹", "'", "’", "(", ")"]


@pytest.mark.parametrize(
    ["value", "expected_result"],
    [
        (r".\tests\hw2\data.txt", [14, "›", tmp_list2, 2972, "ä"]),
    ],
)
def test_task1(value: str, expected_result: Sequence[Any]):
    actual_result1 = get_longest_diverse_words(value)
    shortest_word = min(actual_result1, key=lambda s: len(set(s)))
    tmp_len = len(set(shortest_word))

    actual_result2 = get_rarest_char(value)
    actual_result3 = count_punctuation_chars(value)
    actual_result4 = count_non_ascii_chars(value)
    actual_result5 = get_most_common_non_ascii_char(value)

    assert len(actual_result1) == 10  # retrieve only 10 words
    assert tmp_len == expected_result[0]
    assert actual_result2 == expected_result[1]
    assert actual_result3 == expected_result[2]
    assert actual_result4 == expected_result[3]
    assert actual_result5 == expected_result[4]
