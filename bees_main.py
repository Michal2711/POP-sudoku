import pygame
import time
from utils.constant import WIDTH, HEIGHT, SQUARE_SIZE, MAX_ITER, BEES_AMOUNT, BEES_MOVE
from utils.game import Game
from algorithms.bees.bees import bees_algorithm

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Sudoku')


def solve_sudoku():
    clock = pygame.time.Clock()
    game = Game(WIN)

    game.update()

    start_time = time.time()

    best_bee = bees_algorithm(
            board=game.get_board(),
            game=game,
            max_iterations=MAX_ITER,
            population_size=BEES_AMOUNT,
            bee_moves=BEES_MOVE
    )

    end_time = time.time() - start_time
    print(f"Lasted for: {round(end_time, 2)}s")
    print(f"Cost of best bee is: {best_bee.cost - 1}")

    pygame.time.delay(1000)


if __name__ == "__main__":
    solve_sudoku()