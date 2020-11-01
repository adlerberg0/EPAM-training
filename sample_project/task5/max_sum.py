"""
Given a list of integers numbers "nums".
You need to find a sub-array with length less equal to "k", with maximal sum.
The written function should return the sum of this sub-array.
Examples:
    nums = [1, 3, -1, -3, 5, 3, 6, 7], k = 3
    result = 16
"""
from collections import deque
from typing import List


def find_maximal_sub_array_sum(nums: List[int], k: int) -> int:
    traverse_deq = deque()
    tmp_sum = 0
    max_sum = 0
    # init deq with k values
    for i in range(k):
        traverse_deq.append(nums[i])
        tmp_sum = sum(traverse_deq)
        max_sum = tmp_sum
    # traverse through nums with deq
    for i in range(k, len(nums)):
        traverse_deq.append(nums[i])
        last_elem = traverse_deq.popleft()
        tmp_sum = tmp_sum - last_elem + nums[i]
        if tmp_sum > max_sum:
            max_sum = tmp_sum
    return max_sum
