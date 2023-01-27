import pygame
from constant import WIDTH, HEIGHT, SQUARE_SIZE
from game import Game
from bees import bees_algorithm
from tests_boards.create_board import create_board
from tests_boards.pieces import easy_pieces, medium_pieces, hard_pieces

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Sudoku')


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

board_level_10 = [
    [5, 7, 9, 6, 4, 2, 3, 1, 8],
    [8, 1, 3, 9, 7, 5, 6, 4, 0],
    [2, 4, 6, 3, 1, 8, 9, 7, 5],
    [1, 0, 8, 5, 6, 0, 2, 3, 4],
    [7, 6, 0, 2, 0, 4, 8, 9, 1],
    [4, 3, 2, 8, 9, 1, 5, 6, 7],
    [6, 2, 7, 0, 8, 3, 1, 5, 9],
    [3, 8, 0, 1, 5, 9, 7, 2, 6],
    [9, 0, 1, 7, 2, 6, 4, 8, 3]
]

def solve_sudoku():
    clock = pygame.time.Clock()
    game = Game(WIN)

    board = game.get_board()
    for row_idx, row in enumerate(board_level_10):
        for piece_idx, piece_val in enumerate(row):
            if piece_val == 0:
                board.move(row=row_idx, col=piece_idx, number=None)
            else:
                board.move(row=row_idx, col=piece_idx, number=piece_val)

    #game.board = create_board(pieces=easy_pieces, board=game.get_board())
    game.board = board
    game.update()


    best_bee = bees_algorithm(
            board=game.get_board(),
            game=game,
            max_iterations=100, 
            population_size=10,
            bee_moves=1
    )
    print(f"Cost of best bee is: {best_bee.cost - 2}")

    pygame.time.delay(5000)


if __name__ == "__main__":
    solve_sudoku()