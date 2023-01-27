import pygame
import time
from constant import WIDTH, HEIGHT, SQUARE_SIZE
from game import Game
from bees import bees_algorithm
from tests_boards.create_board import create_board, create_test_board
from tests_boards.pieces import easy_pieces, medium_pieces, hard_pieces
from tests_boards.boards import board_level_10, board_level_20, board_level_30, board_level_40, board_level_50

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Sudoku')


def solve_sudoku():
    clock = pygame.time.Clock()
    game = Game(WIN)

    # game.board = create_test_board(elements=board_level_20, board=game.get_board())

    game.update()

    start_time = time.time()

    best_bee = bees_algorithm(
            board=game.get_board(),
            game=game,
            max_iterations=100,
            population_size=10,
            bee_moves=1
    )

    end_time = time.time() - start_time
    print(f"Lasted for: {round(end_time, 2)}s")
    print(f"Cost of best bee is: {best_bee.cost - 2}")

    pygame.time.delay(100)


if __name__ == "__main__":
    solve_sudoku()