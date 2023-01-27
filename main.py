import pygame
from constant import WIDTH, HEIGHT, SQUARE_SIZE
from game import Game
from algorithm import random_algorithm

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
    game = Game(WIN)

    while run:
        clock.tick(FPS)

        is_move_ok = random_algorithm(game.get_board(), game)

        if is_move_ok is False:
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if game.result is not None:
            print(game.result)
            game.update()
            pygame.time.delay(5000)
            run = False

        if run is True:
            game.update()

        if(len(game.get_board().get_all_empty_pieces()) == 0):
            result = game.board.check_is_board_valid()
            # print("------------")
            # print(game.get_board().final_board)
            # print("------------")
            print(result)
            print(game.board.check_is_board_same())
            pygame.time.delay(10000)
            run = False

    pygame.quit()


if __name__ == "__main__":
    main()