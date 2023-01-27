import pygame
import time
from constant import WIDTH, HEIGHT, SQUARE_SIZE
from game import Game
from bees import bees_algorithm

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
            max_iterations=100,
            population_size=10,
            bee_moves=1
    )

    end_time = time.time() - start_time
    print(f"Lasted for: {round(end_time, 2)}s")
    print(f"Cost of best bee is: {best_bee.cost - 1}")

    pygame.time.delay(100)


if __name__ == "__main__":
    solve_sudoku()