import random

import numpy as np
from constant import BASE, ROWS, COLS, ANT_STEP_RANGE
from copy import deepcopy


class Ant:
    def __init__(self, board, ants):
        self.board = deepcopy(board)
        self.current_position = self.get_random_start_position()
        self.previous_position = self.current_position
        self.ants = ants
        self.number_frequency = {i: 0 for i in range(1, ROWS + 1)}

    def calculate_frequency(self):
        for r in range(ROWS):
            for c in range(COLS):
                number = self.board.get_piece(r, c).number
                if number:
                    self.number_frequency[number] += 1

    def get_random_start_position(self):
        row = random.randint(0, ROWS-1)
        column = random.randint(0, COLS-1)
        return [row, column]

    def move(self):
        best, quality = self.best_move()
        print(f"best: {best}")
        if best is None or len(best.get_valid_numbers()) == 0:
            return None

        self.previous_position = self.current_position

        choosen_number = best.get_valid_numbers()[0] if len(best.get_valid_numbers()) == 1 else random.choice(best.get_valid_numbers())
        self.board.move(best.row, best.col, choosen_number)
        self.current_position = [best.row, best.col]

        if self.check_if_board_is_valid() is False:
            self.go_back()

        # update feromone lever after each move
        best.feromone_level += self.feromone_increment()
        self.update_feromone_level(best)
        return quality  # im mniejsza wartość tym lepsze, najlepiej 1

    def update_feromone_level(self, piece):
        for ant in self.ants:
            if ant != self:
                ant.board.get_piece(piece.row, piece.col).feromone_level += self.feromone_increment()

    def feromone_increment(self):
        return 1 / self.quality_move

    def best_move(self):
        potential_moves = []
        row_min = max(self.current_position[0] - ANT_STEP_RANGE, 0)
        col_min = max(self.current_position[1] - ANT_STEP_RANGE, 0)
        row_max = min(self.current_position[0] + ANT_STEP_RANGE, ROWS - 1)
        col_max = min(self.current_position[1] + ANT_STEP_RANGE, COLS - 1)
        for r in range(row_min, row_max + 1):
            for c in range(col_min, col_max + 1):
                if ((r != self.current_position[0] or c != self.current_position[1]) and self.board.get_piece(r, c).number is None):
                    potential_moves.append(self.board.get_piece(r, c))

        for move in potential_moves:
            valid_numbers = move.get_valid_numbers()
            # Create a dictionary to store the frequency of each number on the board
            frequency = {num: 0 for num in valid_numbers}
            for r in range(9):
                for c in range(9):
                    if self.board.get_piece(r, c).number in frequency:
                        frequency[self.board.get_piece(r, c).number] += 1
            move.weight = sum([1/frequency[num] for num in valid_numbers])

        potential_moves.sort(key=lambda x: x.weight, reverse=True)
        total_feromones = sum([x.feromone_level for x in potential_moves])
        rand = random.uniform(0, total_feromones)

        for move in potential_moves:
            rand -= move.feromone_level
            if rand <= 0:
                best = move
                break

        if potential_moves:
            best = potential_moves[0]
            self.current_position = [best.row, best.col]
            self.quality_move = len(best.get_valid_numbers())
            return best, self.quality_move
        else:
            return None, None

    def go_back(self):
        self.board.board[self.current_position[0]][self.current_position[1]].number = 0
        self.current_position = self.previous_position

    def check_if_board_is_valid(self):
        transpose_board = deepcopy(self.board)
        transpose_board = np.array(transpose_board).T.tolist()
        for r in range(ROWS):
            potential_correct_row = [piece.number for piece in self.board.board[r]]
            potential_T_correct_row = [piece.number for piece in transpose_board.board[r]]
            potential_correct_row = list(filter(lambda num: num != 0, potential_correct_row))
            potential_T_correct_row = list(filter(lambda num: num != 0, potential_T_correct_row))
            if any(potential_correct_row.count(num) > 1 for num in potential_correct_row) or any(potential_T_correct_row.count(num) > 1 for num in potential_T_correct_row):
                return False

        for r in range(0, ROWS, BASE):
            for c in range(0, COLS, BASE):
                if(self.is_square_valid(r, c) is False):
                    return False

        return True

    def is_square_valid(self, row, col):
        square = []
        for r in range(row, row+BASE):
            for c in range(col, col+BASE):
                square.append(self.board.board[r][c].number)
        square = list(filter(lambda num: num != 0, square))
        if any(square.count(num) > 1 for num in square):
            return False
        return True
