"""
Tic Tac Toe Player
"""
import copy

X = "X"
O = "O"
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
    num_of_x = sum(row.count(X) for row in board)
    num_of_o = sum(row.count(O) for row in board)

    return X if num_of_x <= num_of_o else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    return {(i, j) for i in range(3) for j in range(3) if board[i][j] is EMPTY}


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    Raises an exception if the move is invalid.
    """
    i, j = action

    if i < 0 or i >= 3 or j < 0 or j >= 3:
        raise ValueError(f"Invalid move: Cell ({i}, {j}) is out of bounds.")

    if board[i][j] is not EMPTY:
        raise ValueError(f"Invalid move: Cell ({i}, {j}) is already occupied.")

    new_board = copy.deepcopy(board)
    new_board[i][j] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not EMPTY:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] is not EMPTY:
            return board[0][i]

    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not EMPTY:
        return board[0][2]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return winner(board) is not None or all(cell is not EMPTY for row in board for cell in row)


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    result = winner(board)
    if result == X:
        return 1
    elif result == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    turn = player(board)

    if turn == X:
        move = max_value(board)[1]
    else:
        move = min_value(board)[1]

    return move


def max_value(board):
    if terminal(board):
        return utility(board), None

    best_value = float('-inf')
    best_action = None
    for action in actions(board):
        value, _ = min_value(result(board, action))
        if value > best_value:
            best_value = value
            best_action = action
        if best_value == 1:
            break
    return best_value, best_action


def min_value(board):
    if terminal(board):
        return utility(board), None

    best_value = float('inf')
    best_action = None
    for action in actions(board):
        value, _ = max_value(result(board, action))
        if value < best_value:
            best_value = value
            best_action = action
        if best_value == -1:
            break
    return best_value, best_action
