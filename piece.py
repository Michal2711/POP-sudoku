import pygame
from constant import SQUARE_SIZE, BLACK, WHITE, BASE

pygame.font.init()
number_font = pygame.font.SysFont(None, 25)


class Piece:
    """
    class Piece. Contain attributes:
        :param row: row in which piece is located
        :param col: col in which piece is located
        :param number: number seen on the board for piece
        :param valid_number: possible numbers that can be set for piece
        :param x: position of piece (SQUARE_SIZE * col)
        :param y: position of piece (SQUARE_SIZE * row)
    """
    def __init__(self, row, col, number):
        self.row = row
        self.col = col
        self.number = number
        self.valid_numbers = [number for number in range(1, BASE*BASE + 1)]
        self.feromone_numbers_level = dict()
        # self.feromone_level = 0
        self.weight = 0

        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def get_valid_numbers(self):
        return self.valid_numbers

    def get_feromone_numbers_level(self):
        return self.feromone_numbers_level

    def draw(self, win):
        if self.number != 0:
            self.draw_blit(win, self.number)

    def draw_blit(self, win, number):
        number_text = str(number)
        number_image = number_font.render(number_text, True, BLACK, WHITE)
        if(number is not None):
            win.blit(
                number_image,
                (
                    self.x - number_image.get_width()//2,
                    self.y - number_image.get_height()//2
                )
            )

    def __repr__(self):
        return str(f'Piece ({(self.row, self.col)} )with number: {self.number}')
