from typing import  Optional, Tuple, List
from enum import Enum
from dataclasses import dataclass
import random
class Player(Enum):
    X = 0
    O = 1
    
@dataclass
class Board():
    size: int
    cells: List[Optional[Player]]

def initial_board(size: int) -> Board:
    return Board(size, [None for i in range(size * size)])

def player(board: Board) -> Player:
    if sum(1 for c in board.cells if c is None) % 2 == 0:
        return Player.O
    return Player.X

def actions(board: Board) -> list:
    return [i for i in range(len(board.cells)) if board.cells[i] is None]

def result(board: Board, action: int) -> Board:
    return Board(board.size, [board.cells[i] if i != action else player(board) for i in range(len(board.cells))])

def winner(board: Board) -> Optional[Player]:
    for i in range(board.size):
        row = board.cells[i * board.size : (i + 1) * board.size]
        if all(cell is not None and cell == row[0] for cell in row):
            return row[0]
    
    for j in range(board.size):
        col = [board.cells[i * board.size + j] for i in range(board.size)]
        if all(cell is not None and cell == col[0] for cell in col):
            return col[0]
    
    # check diagonal
    diagnal_left = [board.cells[i * board.size + i] for i in range(board.size)]
    diagnal_right = [board.cells[i * board.size + board.size - 1 - i] for i in range(board.size)]
    if all(cell is not None and cell == diagnal_left[0] for cell in diagnal_left):
        return diagnal_left[0]
    if all(cell is not None and cell == diagnal_right[0] for cell in diagnal_right):
        return diagnal_right[0]
    return None

def is_terminal(board: Board) -> bool:
    # check row is full
    if winner(board) is not None:
        return True
    if all(cell is not None for cell in board.cells):
        return True
    return False

def utility(board: Board) -> int:
    if winner(board) == Player.X:
        return 1
    if winner(board) == Player.O:
        return -1
    return 0

def minimax(board: Board) -> Tuple[int, Optional[int]]:
    if is_terminal(board):
        return utility(board), None
    scores = []
    moves = []
    for action in actions(board):
        possible_board = result(board, action)
        scores.append(minimax(possible_board)[0])
        moves.append(action)
    if player(board) == Player.X:
        max_score_index = scores.index(max(scores))
        return scores[max_score_index], moves[max_score_index]
    else:
        min_score_index = scores.index(min(scores))
        return scores[min_score_index], moves[min_score_index]

def draw(board: Board) -> None:
    for i in range(board.size):
        for j in range(board.size):
            if board.cells[i * board.size + j] == Player.X:
                print("X", end=" ")
            elif board.cells[i * board.size + j] == Player.O:
                print("O", end=" ")
            else:
                print("-", end=" ")
        print()



board = initial_board(3)

def player_move() -> int:
    action = int(input("Enter your move: "))
    return action



while not is_terminal(board):
    draw(board)
    action = player_move()
    while action not in actions(board):
        print("Invalid move, try again")
        action = player_move()
    board = result(board, action)
    action = minimax(board)[1]
    board = result(board, action)

draw(board)
if is_terminal(board) == Player.X:
    print("X won")
elif is_terminal(board) == Player.O:
    print("O won")
else:
    print("draw")