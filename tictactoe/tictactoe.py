"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


row_0 = set([(0,0), (0,1), (0,2)])
row_1 = set([(1,0), (1,1), (1,2)])
row_2 = set([(2,0), (2,1), (2,2)])
col_0 = set([(0,0), (1,0), (2,0)])
col_1 = set([(0,1), (1,1), (2,1)])
col_2 = set([(0,2), (1,2), (2,2)])
dia_0 = set([(0,0), (1,1), (2,2)])
dia_1 = set([(0,2), (1,1), (2,0)])
win_states = [row_0, row_1, row_2, col_0, col_1, col_2, dia_0, dia_1]

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
    xs = 0
    os = 0
    for i in board:
        for j in i:
            if j == X:
                xs += 1
            elif j == O:
                os += 1
    if xs == os:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    pos = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                pos.add((i, j))
    return pos


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    print(action, board)
    if action not in actions(board):
        raise Exception("Invalid move")
    p = player(board)
    print(board)
    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = p
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    x_pos_list = []
    o_pos_list = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                x_pos_list.append((i, j))
            elif board[i][j] == O:
                o_pos_list.append((i, j))
    xs = set(x_pos_list)
    os = set(o_pos_list)
    for con in win_states:
        if con.issubset(xs):
            return X
        elif con <= os:
            return O
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    win = winner(board)
    if win != None:
        return True
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0
    
def recursive_minimax(board, is_max):
    if terminal(board):
        return utility(board)
    
    acts = actions(board)
    if is_max:
        high = -math.inf
        for act in acts:
            # print(act)
            new_board = copy.deepcopy(board)
            new_board[act[0]][act[1]] = X
            high = max(high, recursive_minimax(new_board, False))
        return high
    
    else:
        low = math.inf
        for act in acts:
            # print(act)
            new_board = copy.deepcopy(board)
            new_board[act[0]][act[1]] = O
            low = min(low, recursive_minimax(new_board, True))
        return low

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    move = None
    acts = actions(board)
    print(acts)
    if (1, 1) in acts:
        return (1, 1)
    play = player(board)
    is_max = True
    best_value = math.inf
    if play == X:
        is_max = False
        best_value = -math.inf
    for act in acts:
        print(act)
        new_board = copy.deepcopy(board)
        new_board[act[0]][act[1]] = play
        act_value = recursive_minimax(new_board, is_max)
        print(act_value)
        if play == X:
            if act_value > best_value:
                print(act, act_value)
                best_value = act_value
                move = act
        else:
            if act_value < best_value:
                best_value = act_value
                move = act
    print(move)
    return move
