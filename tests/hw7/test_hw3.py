from hw7.hw3 import tic_tac_toe_checker


def test_tic_tac_toe_unfinished_result():
    board = [["-", "-", "o"], ["-", "x", "o"], ["x", "o", "x"]]
    assert tic_tac_toe_checker(board) == "unfinished"


def test_tic_tac_toe_x_wins_in_raw():
    board = [["-", "-", "o"], ["-", "x", "o"], ["x", "x", "x"]]
    assert tic_tac_toe_checker(board) == "x wins!"


def test_tic_tac_toe_x_wins_in_column():
    board = [["x", "-", "o"], ["x", "o", "o"], ["x", "o", "x"]]
    assert tic_tac_toe_checker(board) == "x wins!"


def test_tic_tac_toe_o_wins_in_diagonal():
    board = [["-", "-", "o"], ["-", "o", "x"], ["o", "x", "x"]]
    assert tic_tac_toe_checker(board) == "o wins!"


def test_tic_tac_toe_drows_with_no_explicit_winners():
    board = [["o", "x", "o"], ["x", "o", "x"], ["x", "o", "x"]]
    assert tic_tac_toe_checker(board) == "draw!"


def test_tic_tac_toe_drows_when_both_players_win():
    board = [["x", "x", "o"], ["x", "o", "o"], ["x", "o", "o"]]
    assert tic_tac_toe_checker(board) == "draw!"
