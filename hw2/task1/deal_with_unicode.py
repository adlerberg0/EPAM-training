"""
Given a file containing text. Complete using only default collections:
    1) Find 10 longest words consisting from largest amount of unique symbols
    2) Find rarest symbol for document
    3) Count every punctuation char
    4) Count every non ascii char
    5) Find most common non ascii char for document
"""
import unicodedata
from collections import defaultdict
from itertools import chain
from typing import List


def get_longest_diverse_words(file_path: str) -> List[str]:
    with open(file_path, "r", encoding="unicode-escape", errors="replace") as f:
        long_words = {i: set() for i in range(-10, 0)}
        for line in f:
            word_list = set(line.strip().split())
            for word in word_list:
                cnt_unique = len(set(word))
                min_cnt = min(long_words)
                if cnt_unique >= min_cnt:
                    long_words.setdefault(cnt_unique, set())
                    if word in long_words[cnt_unique]:
                        continue
                    elif len(long_words[min_cnt]) > 1:
                        long_words[min_cnt].pop()
                    else:
                        long_words.pop(min_cnt)
                    long_words.setdefault(cnt_unique, set())
                    long_words[cnt_unique].add(word)

    return set(chain(*long_words.values()))


def get_rarest_char(file_path: str) -> str:
    with open(file_path, "r", encoding="unicode-escape", errors="replace") as f:
        tmp_dict = defaultdict(int)
        for line in f:
            for char in line:
                tmp_dict[char] += 1
    return min(tmp_dict, key=lambda key: tmp_dict[key])


def count_punctuation_chars(file_path: str) -> List[str]:
    with open(file_path, "r", encoding="unicode-escape", errors="replace") as f:
        punct_char_dict = defaultdict(int)
        for line in f:
            # use unicodedata package to find all unicode symbols from section with name started from P
            for char in line:
                if unicodedata.category(char).startswith("P"):
                    punct_char_dict[char] += 1
    return list(punct_char_dict.keys())


def count_non_ascii_chars(file_path: str) -> int:
    with open(file_path, "r", encoding="unicode-escape", errors="replace") as f:
        ascii_num_set = tuple(range(127))
        cnt = 0
        for line in f:
            # count all characters except ascii_num_set
            for char in line:
                if not ord(char) in ascii_num_set:
                    cnt += 1
    return cnt


def get_most_common_non_ascii_char(file_path: str) -> str:
    with open(file_path, "r", encoding="unicode-escape", errors="replace") as f:
        tmp_dict = defaultdict(int)
        for line in f:
            ascii_num_set = {k for k in range(127)}
            # evaluate all characters except ascii_num_set
            for char in line:
                if not ord(char) in ascii_num_set:
                    tmp_dict[char] += 1
    return max(tmp_dict, key=lambda key: tmp_dict[key])
