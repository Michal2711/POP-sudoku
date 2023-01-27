from copy import deepcopy
from constant import WHITE
import pygame
import random

pygame.font.init()
number_font = pygame.font.SysFont(None, 25)


def random_algorithm(board, game):
    min_posibilities = 9
    all_empty_pieces = board.get_all_empty_pieces()
    for piece in all_empty_pieces:
        possibilities = len(piece.valid_numbers)
        if possibilities == 0:
            return False
        # temp_board = deepcopy(board)
        # draw_posibilities(game, temp_board, piece, possibilities)
        if possibilities < min_posibilities:
            min_posibilities = possibilities
            choosen_piece = piece
            if possibilities == 1:
                choosen_number = random.choice(choosen_piece.valid_numbers)
                simulate_move(board, choosen_piece, choosen_number)
                return True

    pygame.time.delay(300)

    choosen_number = random.choice(choosen_piece.valid_numbers)
    simulate_move(board, choosen_piece, choosen_number)

    return True


def simulate_move(board, piece, number):
    board.move(piece.row, piece.col, number)


def draw_posibilities(game, board, piece, posibilities):
    size_of_valid_numbers = str(posibilities)
    posibilities_image = number_font.render(size_of_valid_numbers, True, (255, 0, 0), WHITE)
    game.win.blit(
        posibilities_image,
        (
            piece.x - posibilities_image.get_width()//2,
            piece.y - posibilities_image.get_height()//2
        )
    )
    pygame.display.update()
    pygame.time.delay(200)
