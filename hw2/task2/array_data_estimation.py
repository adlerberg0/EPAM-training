"""
Given an array of size n, find the most common and the least common elements.
The most common element is the element that appears more than n // 2 times.
The least common element is the element that appears fewer than other.

You may assume that the array is non-empty and the most common element
always exist in the array.

Example 1:

Input: [3,2,3]
Output: 3, 2

Example 2:

Input: [2,2,1,1,1,2,2]
Output: 2, 1

"""
from collections import defaultdict
from typing import List, Tuple


def major_and_minor_elem(inp: List) -> Tuple[int, int]:
    # use dict to find the most and the least frequently faced element in array
    d = defaultdict(int)
    for item in inp:
        d[item] += 1
    min_freq_elem = min(d, key=lambda key: d[key])
    max_freq_elem = max(d, key=lambda key: d[key])
    return max_freq_elem, min_freq_elem
