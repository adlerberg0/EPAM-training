"""
Write a function that merges integer from sorted files and returns an iterator
file1.txt:
1
3
5
file2.txt:
2
4
6
#>>> list(merge_sorted_files(["file1.txt", "file2.txt"]))
#[1, 2, 3, 4, 5, 6]
"""
from pathlib import Path
from typing import Iterator, List, Union


def merge_helping_func(data_list: list) -> list:
    list_len = len(data_list)
    if list_len <= 1:
        return data_list
    mid = list_len // 2

    left_half = merge_helping_func(data_list[0:mid])
    right_half = merge_helping_func(data_list[mid:])

    left_marker = 0
    right_marker = 0
    marker = 0
    res = [0] * list_len
    while left_marker < len(left_half) and right_marker < len(right_half):
        if left_half[left_marker] <= right_half[right_marker]:
            res[marker] = left_half[left_marker]
            marker += 1
            left_marker += 1
        else:
            res[marker] = right_half[right_marker]
            marker += 1
            right_marker += 1
    while left_marker < len(left_half):
        res[marker] = left_half[left_marker]
        marker += 1
        left_marker += 1
    while right_marker < len(right_half):
        res[marker] = right_half[right_marker]
        marker += 1
        right_marker += 1
    return res


def merge_sorted_files(file_list: List[Union[Path, str]]) -> Iterator:
    file_path1 = Path(file_list[0])
    file_path2 = Path(file_list[1])

    if not file_path1.is_file():
        raise FileNotFoundError
    if not file_path2.is_file():
        raise FileNotFoundError
    first_file = []
    second_file = []
    with open(file_path1) as fi:
        for line in fi:
            first_file.append(int(line))
    with open(file_path2) as fi:
        for line in fi:
            second_file.append(int(line))

    res = merge_helping_func(first_file + second_file)
    return iter(res)
