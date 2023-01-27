import pygame
import numpy as np
from copy import deepcopy
from constant import ROWS, SQUARE_SIZE, COLS, WHITE, BLACK, HEIGHT, BASE, LEVEL_PARAM_1, LEVEL_PARAM_2
from random import sample
from piece import Piece
from boards_test.test_boards import get_board


class Board:
    """
    class Board. Contain attributes:
        :param board: list of lists of Piece objects containt current version of out board
        :param final_board: board that include generated version of board
        :param filled_fields: number of filled field of current board
    """
    def __init__(self):
        self.board = []
        self.final_board = []
        self.create_board()
        self.filled_fields = 0

    def create_board(self):
        # self.generate_full_board()
        # self.final_board = deepcopy(self.board)
        # self.delete_part_board()

        board_pieces = []

        self.board = get_board()

        for row in range(ROWS):
            board_pieces.append([])
            for col in range(COLS):
                if self.board[row][col] != 0:
                    board_pieces[row].append(Piece(row, col, self.board[row][col]))
                else:
                    board_pieces[row].append(Piece(row, col, None))
        self.board = board_pieces

        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col].number is None:
                    self.calculate_valid_numbers(self.board[row][col])
                else:
                    self.board[row][col].valid_numbers = [self.board[row][col].number]

    def draw_squares(self, win):
        win.fill(WHITE)
        for row in range(ROWS-1):
            if(row % BASE == BASE - 1):
                pygame.draw.line(win, BLACK, (0, row*SQUARE_SIZE + SQUARE_SIZE), (HEIGHT, row*SQUARE_SIZE + SQUARE_SIZE), 4)
                pygame.draw.line(win, BLACK, (row*SQUARE_SIZE + SQUARE_SIZE, 0), (row*SQUARE_SIZE + SQUARE_SIZE, HEIGHT), 4)
            pygame.draw.line(win, BLACK, (0, row*SQUARE_SIZE + SQUARE_SIZE), (HEIGHT, row*SQUARE_SIZE + SQUARE_SIZE), 1)
            pygame.draw.line(win, BLACK, (row*SQUARE_SIZE + SQUARE_SIZE, 0), (row*SQUARE_SIZE + SQUARE_SIZE, HEIGHT), 1)

    def get_all_pieces(self):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece.number is not None:
                    pieces.append(piece)
        return pieces

    def get_all_empty_pieces(self):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece.number is None:
                    pieces.append(piece)
        return pieces

    def move(self, row, col, number):
        self.board[row][col] = Piece(row, col, number)
        self.filled_fields += 1
        self.update_valid_numbers(self.board[row][col])

    def update_valid_numbers(self, piece):
        row = piece.row
        col = piece.col

        for c in range(COLS):
            if self.board[row][c].number is None and piece.number in self.board[row][c].valid_numbers:
                self.board[row][c].valid_numbers.remove(piece.number)
                self.board[row][c].feromone_numbers_level.pop(piece.number)

        for r in range(ROWS):
            if self.board[r][col].number is None and piece.number in self.board[r][col].valid_numbers:
                self.board[r][col].valid_numbers.remove(piece.number)
                self.board[r][col].feromone_numbers_level.pop(piece.number)

        start_row = row - (row % BASE)
        start_col = col - (col % BASE)
        end_row = start_row + BASE - 1
        end_col = start_col + BASE - 1

        for r in range(start_row, end_row + 1):
            for c in range(start_col, end_col + 1):
                if self.board[r][c].number is None and piece.number in self.board[r][c].valid_numbers:
                    self.board[r][c].valid_numbers.remove(piece.number)
                    self.board[r][c].feromone_numbers_level.pop(piece.number)

    def get_piece(self, row, col):
        return self.board[row][col]

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def shuffle(self, s):
        return sample(s, len(s))

    def pattern(self, r, c):
        return (BASE*(r % BASE)+r // BASE + c) % ROWS

    def generate_full_board(self):
        rBase = range(BASE)
        rows = [g*BASE + r for g in self.shuffle(rBase) for r in self.shuffle(rBase)]
        cols = [g*BASE + c for g in self.shuffle(rBase) for c in self.shuffle(rBase)]
        nums = self.shuffle(range(1, BASE*BASE+1))

        self.board = [[nums[self.pattern(r, c)] for c in cols] for r in rows]

    def delete_part_board(self):
        squares = ROWS*ROWS
        empties = squares * LEVEL_PARAM_1 // LEVEL_PARAM_2
        for p in sample(range(squares), empties):
            self.board[p // ROWS][p % ROWS] = 0

    def calculate_valid_numbers(self, piece):
        row = piece.row
        col = piece.col

        if piece.number is not None:
            return [piece.number]

        for c in range(COLS):
            if self.board[row][c].number is not None and self.board[row][c].number in piece.valid_numbers:
                piece.valid_numbers.remove(self.board[row][c].number)

        for r in range(ROWS):
            if self.board[r][col].number is not None and self.board[r][col].number in piece.valid_numbers:
                piece.valid_numbers.remove(self.board[r][col].number)

        start_row = row - (row % BASE)
        start_col = col - (col % BASE)
        end_row = start_row + BASE - 1
        end_col = start_col + BASE - 1

        for r in range(start_row, end_row + 1):
            for c in range(start_col, end_col + 1):
                if self.board[r][c].number is not None and self.board[r][c].number in piece.valid_numbers:
                    piece.valid_numbers.remove(self.board[r][c].number)

        piece.feromone_numbers_level = dict.fromkeys(piece.valid_numbers, 1/len(piece.valid_numbers))

    def check_is_piece_valid(self, piece):
        r = piece.row
        c = piece.col
        if piece.number != self.final_board[r][c]:
            return False
        else:
            return True

    def check_is_board_same(self):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col].number != self.final_board[row][col]:
                    return False
        return True

    def is_square_valid(self, row, col, correct):
        square = []
        for r in range(row, row+BASE):
            for c in range(col, col+BASE):
                square.append(self.board[r][c].number)
        square.sort()
        if (square != correct):
            return False
        return True

    def check_is_board_valid(self):
        correct = [number for number in range(1, BASE*BASE + 1)]
        transpose_board = deepcopy(self.board)
        transpose_board = np.array(transpose_board).T.tolist()
        for r in range(ROWS):
            potential_correct_row = [piece.number for piece in self.board[r]]
            potential_T_correct_row = [piece.number for piece in transpose_board[r]]
            potential_correct_row.sort()
            potential_T_correct_row.sort()
            if potential_correct_row != correct or potential_T_correct_row != correct:
                return False
        for r in range(0, ROWS, BASE):
            for c in range(0, COLS, BASE):
                if(self.is_square_valid(r, c, correct) is False):
                    return False

        return True
