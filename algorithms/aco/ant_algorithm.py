from utils.constant import ROWS
import pygame

pygame.font.init()
number_font = pygame.font.SysFont(None, 25)


def ACO(ants):
    best_quality_board = ROWS + 1
    best_ant_id = 0
    for id in range(len(ants)):
        # ant move
        quality = ants[id].move()
        if quality is not None and quality < best_quality_board:
            best_ant_id = id
            best_quality_board = quality

    # if board is filled
    if ants[best_ant_id].board.filled_fields == ROWS*COLS:
        return ants[best_ant_id].board

    # if all ants failed
    if best_quality_board == ROWS + 1:
        print("NONE")
        return None
    else:
        return ants[best_ant_id].board
