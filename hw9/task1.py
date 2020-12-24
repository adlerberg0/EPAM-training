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

    return iter(sorted(first_file + second_file))
