"""
Classic task, a kind of walnut for you
Given four lists A, B, C, D of integer values,
    compute how many tuples (i, j, k, l) there are such that
     A[i] + B[j] + C[k] + D[l] is zero.
We guarantee, that all A, B, C, D have same length of N where 0 ≤ N ≤ 1000.
"""
from collections import defaultdict
from typing import List


def check_sum_of_four(a: List[int], b: List[int], c: List[int], d: List[int]) -> int:
    """
    1. Merge 4 lists to 2 sets each containing
       all possible sums from 1,2 and 3,4 list respectively
    2. Check whether set2 contain each elem with opposite sign
    Time complexity is N^2
    """
    n = len(a)
    dict1 = defaultdict(int)
    dict2 = defaultdict(int)
    cnt = 0
    for i in range(n):
        for j in range(n):
            dict1[a[i] + b[j]] += 1
            dict2[c[i] + d[j]] += 1

    for key in dict1:
        while dict1[key] > 0:
            for i in range(dict2[-key]):
                cnt += 1
            dict1[key] -= 1
    return cnt
