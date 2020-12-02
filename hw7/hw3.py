"""
Given a Tic-Tac-Toe 3x3 board (can be unfinished).
Write a function that checks if the are some winners.
If there is "x" winner, function should return "x wins!"
If there is "o" winner, function should return "o wins!"
If there is a draw, function should return "draw!"
If board is unfinished, function should return "unfinished!"
Example:
    [[-, -, o],
     [-, x, o],
     [x, o, x]]
    Return value should be "unfinished"
    [[-, -, o],
     [-, o, o],
     [x, x, x]]
     Return value should be "x wins!"
"""
from typing import List

import numpy

SCORE_FOR_X = 1
SCORE_FOR_O = 10
SCORE_FOR_EMPTY_CELL = -300  # should be negative


def custom_sum(board_data: list) -> int:
    score_sum = 0
    for item in board_data:
        if item == "-":
            score_sum += SCORE_FOR_EMPTY_CELL
        elif item == "o":
            score_sum += SCORE_FOR_O
        elif item == "x":
            score_sum += SCORE_FOR_X
    return score_sum


def tic_tac_toe_checker(board: List[List]) -> str:
    arr = numpy.array(board)
    res = []
    # check all rows
    res.extend(list(map(custom_sum, arr)))
    # check all columns
    res.extend(list(map(custom_sum, arr.transpose())))
    # check 2 diagonals
    res.extend(list(map(custom_sum, [arr.diagonal(), arr[::, ::-1].diagonal()])))
    # calc sum for negative value check
    score_sum = sum(res)
    if SCORE_FOR_X * 3 in res and SCORE_FOR_O * 3 in res:
        return "draw!"
    if SCORE_FOR_X * 3 in res:
        return "x wins!"
    elif SCORE_FOR_O * 3 in res:
        return "o wins!"
    elif score_sum > 0:
        return "draw!"
    else:
        return "unfinished"
