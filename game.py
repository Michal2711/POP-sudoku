import pygame
from board import Board


class Game:
    """
    class Game. Contain attributes:
        :param win: window of game
        :param type: pygame.Surface
    """
    def __init__(self, win):
        self._init()
        self.win = win
        self.board.draw(self.win)
        self.result = None
        self.valid_numbers = {}

    def update(self):
        self.board.draw(self.win)
        pygame.display.update()

    def _init(self):
        self.board = Board()

    def get_board(self):
        return self.board
