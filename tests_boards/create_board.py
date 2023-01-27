from typing import List
from board import Board


def create_board(pieces: List, board: Board) -> Board:
    for row, column, value in pieces:
        board.move(row=row, col=column, number=value)
    return board    

