import pygame
from utils.constant import WIDTH, HEIGHT
from utils.game import Game
from algorithms.genetic.genetic import genetic_algorithm


FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Sudoku')


def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    pygame.display.update()

    board = genetic_algorithm(game.get_board())
    board.draw(WIN)
    # game.board = board
    pygame.display.update()
    input()


if __name__ == "__main__":
    main()
