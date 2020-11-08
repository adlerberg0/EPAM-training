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
from typing import List


def get_longest_diverse_words(file_path: str) -> List[str]:
    with open(file_path, encoding="unicode-escape") as f:
        file_s = f.read()
        word_list = file_s.strip().split()
        word_list = list(dict.fromkeys(word_list))
        unique_char_dict = {}
        # calculate amount of unique chars for each word and init dict key with it
        for item in word_list:
            if len(set(item)) in unique_char_dict:
                unique_char_dict[len(set(item))].append(item)
            else:
                unique_char_dict[len(set(item))] = [item]
        finished = False
        res_list = []
        words_remains = 10
        # find the longest words for each key starting from the max(unique_char_dict)
        while not finished:
            max_idx = max(unique_char_dict)
            tmp = sorted(
                unique_char_dict.pop(max_idx), key=lambda s: len(s), reverse=True
            )
            words_remains -= len(tmp)
            if words_remains < 0:
                res_list.extend(tmp[:words_remains])
                finished = True
            else:
                res_list.extend(tmp)
    return res_list


def get_rarest_char(file_path: str) -> str:
    with open(file_path, encoding="unicode-escape") as f:
        file_s = f.read().strip()
        tmp_dict = defaultdict(int)
        for char in file_s:
            tmp_dict[char] += 1
    return min(tmp_dict, key=lambda key: tmp_dict[key])


def count_punctuation_chars(file_path: str) -> List[str]:
    with open(file_path, encoding="unicode-escape") as f:
        file_s = f.read().strip()
        punct_char_dict = defaultdict(int)
        # use unicodedata package to find all unicode symbols from section with name started from P
        for char in file_s:
            if unicodedata.category(char).startswith("P"):
                punct_char_dict[char] += 1
    return list(punct_char_dict.keys())


def count_non_ascii_chars(file_path: str) -> int:
    with open(file_path, encoding="unicode-escape") as f:
        file_s = f.read().strip()
        ascii_num_set = {k for k in range(127)}
        cnt = 0
        # count all characters except ascii_num_set
        for char in file_s:
            if not ord(char) in ascii_num_set:
                cnt += 1
    return cnt


def get_most_common_non_ascii_char(file_path: str) -> str:
    with open(file_path, encoding="unicode-escape") as f:
        file_s = f.read().strip()
        tmp_dict = defaultdict(int)
        ascii_num_set = {k for k in range(127)}
        # evaluate all characters except ascii_num_set
        for char in file_s:
            if not ord(char) in ascii_num_set:
                tmp_dict[char] += 1
    return max(tmp_dict, key=lambda key: tmp_dict[key])
