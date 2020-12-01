import pathlib
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
path_to_file = pathlib.Path(".").joinpath("tests", "hw2", "data.txt")


@pytest.mark.parametrize("value", [path_to_file])
@pytest.mark.parametrize("expected_result", [14])
def test_task1_func1(value: str, expected_result: int):
    actual_result1 = get_longest_diverse_words(value)
    shortest_word = min(actual_result1, key=lambda s: len(set(s)))
    tmp_len = len(set(shortest_word))

    assert len(actual_result1) == 10  # retrieve only 10 words
    assert tmp_len == expected_result


@pytest.mark.parametrize("value", [path_to_file])
@pytest.mark.parametrize("expected_result", ["›"])
def test_get_rarest_char(value: str, expected_result: str):
    actual_result2 = get_rarest_char(value)

    assert actual_result2 == expected_result


@pytest.mark.parametrize("value", [path_to_file])
@pytest.mark.parametrize("expected_result", [tmp_list2])
def test_count_punctuation_chars(value: str, expected_result: Sequence[Any]):
    actual_result = count_punctuation_chars(value)

    assert actual_result == expected_result


@pytest.mark.parametrize("value", [path_to_file])
@pytest.mark.parametrize("expected_result", [2972])
def test_count_non_ascii_chars(value: str, expected_result: int):
    actual_result = count_non_ascii_chars(value)

    assert actual_result == expected_result


@pytest.mark.parametrize("value", [path_to_file])
@pytest.mark.parametrize("expected_result", ["ä"])
def test_get_most_common_non_ascii_char(value: str, expected_result: str):
    actual_result5 = get_most_common_non_ascii_char(value)

    assert actual_result5 == expected_result
