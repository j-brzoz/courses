"""
Tic Tac Toe Player
"""

import math
import copy

x = "X"
o = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = 0
    o_count = 0

    for row in range(3):
        for cell in range(3):
            if board[row][cell] == x:
                x_count += 1
            elif board[row][cell] == o:
                o_count += 1

    if x_count > o_count:
        return o
    else:
        return x


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = []

    for row in range(3):
        for cell in range(3):
            if board[row][cell] == EMPTY:
                possible_actions.append((row, cell))

    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board_copy = copy.deepcopy(board)
    turn = player(board)

    if (action[0] not in range(3) or action[1] not in range(3) or
       board_copy[action[0]][action[1]] != EMPTY):
        raise Exception("action not allowed")
    else:
        board_copy[action[0]][action[1]] = turn

    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # checks rows and columns
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != EMPTY:
            return board[i][0]
        elif (board[0][i] == board[1][i] == board[2][i] and
              board[0][i] != EMPTY):
            return board[0][i]

    # check diagonals
    if (board[0][0] == board[1][1] == board[2][2] or
       board[0][2] == board[1][1] == board[2][0]) and board[1][1] != EMPTY:
        return board[1][1]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # checks for draw
    count = 0
    for row in range(3):
        for cell in range(3):
            if board[row][cell] != EMPTY:
                count += 1

    if winner(board) is not None or count == 9:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    result = winner(board)
    if result == x:
        return 1
    elif result == o:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if player(board) == x:
        if terminal(board):
            return utility(board)
        best_value = -math.inf
        best_action = None
        for action in actions(board):
            value = min_value(result(board, action))
            if best_value < value:
                best_value = value
                best_action = action
        return best_action
    else:
        if terminal(board):
            return utility(board)
        best_value = math.inf
        best_action = None
        for action in actions(board):
            value = max_value(result(board, action))
            if best_value > value:
                best_value = value
                best_action = action
        return best_action


def min_value(board):
    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v


def max_value(board):
    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v
