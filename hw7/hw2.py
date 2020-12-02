"""
Given two strings. Return if they are equal when both are typed into
empty text editors. # means a backspace character.
Note that after backspacing an empty text, the text will continue empty.
Examples:
    Input: s = "ab#c", t = "ad#c"
    Output: True
    # Both s and t become "ac".
    Input: s = "a##c", t = "#a#c"
    Output: True
    Explanation: Both s and t become "c".
    Input: a = "a#c", t = "b"
    Output: False
    Explanation: s becomes "c" while t becomes "b".
"""
from functools import reduce


def backspace_accumulate(accumulate_string: str, next_char: str) -> str:
    if next_char == "#" and accumulate_string != "#":
        return accumulate_string[:-1]
    elif accumulate_string == "#":
        return "" if next_char == "#" else next_char
    return "".join([accumulate_string, next_char])


def backspace_compare(first: str, second: str) -> bool:
    return reduce(backspace_accumulate, first) == reduce(backspace_accumulate, second)
