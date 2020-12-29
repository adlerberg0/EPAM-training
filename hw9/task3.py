"""
Write a function that takes directory path, a file extension and an optional tokenizer.
It will count lines in all files with that extension if there are no tokenizer.
If a the tokenizer is not none, it will count tokens.
For dir with two files from hw1.py:
>>> universal_file_counter(test_dir, "txt")
6
>>> universal_file_counter(test_dir, "txt", str.split)
6
"""
from pathlib import Path
from typing import Callable, Optional


def universal_file_counter(
    dir_path: Path, file_extension: str, tokenizer: Optional[Callable] = None
) -> int:
    cnt = 0
    if not dir_path.is_dir():
        raise NotADirectoryError
    for file in dir_path.rglob(f"*{file_extension}"):
        with open(file) as fi:
            for line in fi:
                if line == "\n":
                    continue
                if not tokenizer:
                    cnt += 1
                else:
                    for token in tokenizer(line):
                        cnt += 1
    return cnt
