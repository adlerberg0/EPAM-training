"""
Some of the functions have a bit cumbersome behavior when we deal with
positional and keyword arguments.

Write a function that accept any iterable of unique values and then
it behaves as range function:


import string


assert = custom_range(string.ascii_lowercase, 'g') == ['a', 'b', 'c', 'd', 'e', 'f']
assert = custom_range(string.ascii_lowercase, 'g', 'p') == ['g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o']
assert = custom_range(string.ascii_lowercase, 'p', 'g', -2) == ['p', 'n', 'l', 'j', 'h']

"""
from typing import Any, Sequence


def custom_range(chars: Sequence[Any], *args: Sequence[Any]) -> Sequence[Any]:
    # bind chars and their indexes
    idx_dict = {}
    for i, item in enumerate(chars):
        idx_dict[item] = i
    # init indexes for range
    args_len = len(args)
    first_idx = 0
    last_idx = 0
    step = 1
    # depending on using case choose slicing indexes
    if args_len == 1:
        last_idx = idx_dict[args[0]]
    elif args_len == 2:
        first_idx = idx_dict[args[0]]
        last_idx = idx_dict[args[1]]
    elif args_len == 3:
        first_idx = idx_dict[args[0]]
        last_idx = idx_dict[args[1]]
        step = int(args[2])
    return list(chars[first_idx:last_idx:step])
