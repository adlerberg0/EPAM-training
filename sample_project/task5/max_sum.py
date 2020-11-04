"""
Given a list of integers numbers "nums".
You need to find a sub-array with length less equal to "k", with maximal sum.
The written function should return the sum of this sub-array.
Examples:
    nums = [1, 3, -1, -3, 5, 10,300, 6, 7], k = 3
    result = 16
"""
from collections import deque
from typing import List


def find_maximal_sub_array_sum(nums: List[int], k: int) -> int:
    traverse_deq = deque()
    max_sum = None
    tmp_sum = 0
    cnt = 0
    for i, item in enumerate(nums):
        # init temp_sum or check item when deq was cleared
        if cnt == 0:
            traverse_deq.append(item)
            tmp_sum = item
            if max_sum is None:
                max_sum = item
            elif item > max_sum:
                max_sum = item
            cnt += 1
        # from 1 to k elements in deq
        elif cnt < k:
            if item + tmp_sum >= tmp_sum:
                traverse_deq.append(item)
                cnt += 1
                tmp_sum += item
                if tmp_sum > max_sum:
                    max_sum = tmp_sum
            else:
                cnt = 0
                traverse_deq.clear()
                if tmp_sum > max_sum:
                    max_sum = tmp_sum
                if (
                    item > max_sum
                ):  # this condition is used for the case when cnt == 1 and we get there
                    max_sum = item
        # deq is full
        else:
            # check if it worth moving deq window
            if item + tmp_sum > tmp_sum:
                traverse_deq.append(item)
                last_elem = traverse_deq.popleft()
                tmp_sum = tmp_sum + item - last_elem
                if tmp_sum > max_sum:
                    max_sum = tmp_sum
            # otherwise clear deq and save sum
            else:
                cnt = 0
                tmp_sum = sum(traverse_deq)
                traverse_deq.clear()
                if tmp_sum > max_sum:
                    max_sum = tmp_sum
    return max_sum
