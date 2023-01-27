from typing import List
from board import Board


def create_board(pieces: List, board: Board) -> Board:
    for row, column, value in pieces:
        board.move(row=row, col=column, number=value)
    return board   

def create_test_board(elements: List, board: Board) -> Board:
    for row_idx, row in enumerate(elements):
        for piece_idx, piece_val in enumerate(row):
            if piece_val == 0:
                board.move(row=row_idx, col=piece_idx, number=None)
            else:
                board.move(row=row_idx, col=piece_idx, number=piece_val) 
    return board

