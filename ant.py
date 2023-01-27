import random

from constant import ROWS, COLS, ANT_STEP_RANGE, WHITE
from copy import deepcopy

import pygame

pygame.font.init()
number_font = pygame.font.SysFont(None, 25)


class Ant:
    def __init__(self, board, ants, game):
        self.board = deepcopy(board)
        self.current_position = self.get_random_start_position()
        self.previous_position = self.current_position
        self.ants = ants
        self.game = game
        self.color = (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))

    def get_random_start_position(self):
        row = random.randint(0, ROWS-1)
        column = random.randint(0, COLS-1)
        return [row, column]

    def move(self):
        best, quality = self.best_move()
        if best is None or len(best.get_valid_numbers()) == 0:
            return None

        possible_fer = max(best.get_feromone_numbers_level().values())
        possible_keys = [k for k, v in best.get_feromone_numbers_level().items() if v == possible_fer]

        if len(possible_keys) > 1:
            freq_prob = []
            choosen_number = 0
            # min_freq = ROWS
            for number in possible_keys:
                freq = self.calculate_freq_number(number)
                freq_prob.append(ROWS - freq)
                # if freq < min_freq:
                #     min_freq = freq
                #     choosen_number = number
            # print(freq_prob)
            freq_prob = [prob/sum(freq_prob) for prob in freq_prob]
            # print(freq_prob)
            choosen_number = random.choices(possible_keys, weights=freq_prob, k=1)[0]

        else:
            choosen_number = possible_keys[0]

        self.board.move(best.row, best.col, choosen_number)
        self.current_position = [best.row, best.col]

        # update feromone lever after each move
        self.update_feromone_level(best, choosen_number)
        return quality

    def update_feromone_level(self, piece, number):
        piece.get_feromone_numbers_level()[number] += 1/self.quality_move
        for ant in self.ants:
            if ant != self:
                if number in ant.board.get_piece(piece.row, piece.col).get_feromone_numbers_level().keys():
                    ant.board.get_piece(piece.row, piece.col).get_feromone_numbers_level()[number] += 1 / self.quality_move

    def best_move(self):
        potential_moves = self.get_all_moves()

        potential_moves.sort(key=lambda x: len(x.get_valid_numbers()), reverse=False)

        if potential_moves:
            best = potential_moves[0]
            self.current_position = [best.row, best.col]
            self.quality_move = len(best.get_valid_numbers())
            return best, self.quality_move
        else:
            return None, None

    def calculate_freq_number(self, number):
        counter = 0
        for r in range(ROWS):
            for c in range(COLS):
                if self.board.get_piece(r, c) is not None and self.board.get_piece(r, c).number == number:
                    counter += 1
        return counter

    def get_all_moves(self):
        moves = []
        row_min = max(self.current_position[0] - ANT_STEP_RANGE, 0)
        col_min = max(self.current_position[1] - ANT_STEP_RANGE, 0)
        row_max = min(self.current_position[0] + ANT_STEP_RANGE, ROWS - 1)
        col_max = min(self.current_position[1] + ANT_STEP_RANGE, COLS - 1)
        for r in range(row_min, row_max + 1):
            for c in range(col_min, col_max + 1):
                if ((r != self.current_position[0] or c != self.current_position[1]) and self.board.get_piece(r, c).number is None):
                    moves.append(self.board.get_piece(r, c))
        return moves

    def draw_posibilities(self, board, piece, posibilities):
        size_of_valid_numbers = str(posibilities)
        posibilities_image = number_font.render(size_of_valid_numbers, True, self.color, WHITE)
        self.game.win.blit(
            posibilities_image,
            (
                piece.x - posibilities_image.get_width()//2,
                piece.y - posibilities_image.get_height()//2
            )
        )
        pygame.display.update()
        # pygame.time.delay(500)
