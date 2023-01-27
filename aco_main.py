import pygame
import time
from boards_test.test_boards import get_board
from utils.constant import WIDTH, HEIGHT, SQUARE_SIZE, NUMBER_OF_ANTS
from utils.game import Game
from algorithms.aco.ant_algorithm import ACO
from algorithms.aco.ant import Ant

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Sudoku')


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def main():

    run = True
    clock = pygame.time.Clock()
    start_time = time.time()
    game = Game(WIN)

    while run:
        clock.tick(FPS)

        ants = []
        for _ in range(NUMBER_OF_ANTS):
            ants.append(Ant(game.get_board(), ants, game))

        new_board = ACO(ants)
        if new_board is None:
            pygame.time.delay(2000)
            print("Nie udało się rozwiązać sudoku")
            run = False
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
            print("--- %s seconds ---" % (time.time() - start_time))
            run = False

    pygame.quit()


if __name__ == "__main__":
    main()
