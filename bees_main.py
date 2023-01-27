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


def solve_easy_sudoku():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    game.board = create_board(pieces=easy_pieces, board=game.get_board())

    while run:
        clock.tick(FPS)

        new_board = bees_algorithm(
            board=game.get_board(), 
            game=game, 
            max_iterations=10, 
            population_size=20,
            bee_moves=20
        )

        if new_board is None:
            print("Could not solved sudoku")
            run = False
            pygame.time.delay(10000)
            pygame.quit()
        else:
            game.board = new_board

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if game.result is not None:
            print(game.result)
            game.update()
            run = False

        if run is True:
            game.update()

        if(len(game.get_board().get_all_empty_pieces()) == 0):
            result = game.board.check_is_board_valid()
            print(f"Is board valid: {result}")
            print(f"Is board same as generated {game.board.check_is_board_same()}")
            pygame.time.delay(10000)
            run = False


if __name__ == "__main__":
    solve_easy_sudoku()