"""
Given a dictionary (tree), that can contains multiple nested structures.
Write a function, that takes element and finds the number of occurrences
of this element in the tree.
Tree can only contains basic structures like:
    str, list, tuple, dict, set, int, bool
"""
from typing import Any


def tree_traverse(tree: Any, element: Any) -> int:
    cnt = 0
    # base - non recursive object
    if isinstance(tree, (str, int, bool)):
        return 1 if tree == element else 0
    if isinstance(tree, dict):
        # recursive dict object
        for key, value in tree.items():
            if key == element:
                cnt += 1
            if value == element:  # do not pass value to recursion
                cnt += 1
            else:
                cnt += tree_traverse(value, element)
    else:
        # recursive non dict object
        for item in tree:
            if item == element:
                cnt += 1
            else:
                cnt += tree_traverse(item, element)
    return cnt


def find_occurrences(tree: dict, element: Any) -> int:
    return tree_traverse(tree, element)
