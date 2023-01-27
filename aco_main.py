import pygame
import time
from utils.constant import WIDTH, HEIGHT, NUMBER_OF_ANTS
from utils.game import Game
from algorithms.aco.ant_algorithm import ACO
from algorithms.aco.ant import Ant

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Sudoku')


def main():

    run = True
    clock = pygame.time.Clock()
    start_time = time.time()
    game = Game(WIN)

    while run:
        clock.tick(FPS)

        # generate ants
        ants = []
        for _ in range(NUMBER_OF_ANTS):
            ants.append(Ant(game.get_board(), ants))

        # getting best ant board from algorithm
        new_board = ACO(ants)
        if new_board is None:
            pygame.time.delay(2000)
            print("Failed to solve sudoku")
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
