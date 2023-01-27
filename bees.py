import random
from copy import deepcopy
import pygame
import random
from typing import List, Tuple

from board import Board
from game import Game

"""
initialize randomly scout bees;
while sudoku is not solved:
    evaluate bees cells; //from heuristic function
    select bees with high fitnesses;
    go to selected bees cells;
    search through selected bees cells with remaining bees;
"""

class Bee():
    def __init__(self, position: Tuple[int], cost: int, board: Board) -> None:
        self.position = position
        self.cost = cost
        self.board = deepcopy(board)

    def move(self, value):
        self.board.move(row=self.position[0], col=self.position[1], number=value)


def initialize_random_bee(board: Board, game: Game) -> List[Bee] | None:
    possible_pieces = board.get_possibile_pieces()
    if possible_pieces:
        random_piece = random.choice(possible_pieces)
        random_bee = Bee(position=(random_piece.row, random_piece.col), cost=len(possible_pieces), board=board)
        random_bee.move(value=random_piece.number)
        return random_bee
    return None


def create_neighbour(bee: Bee) -> Bee:
    possible_pieces = bee.board.get_possibile_pieces()
    if possible_pieces:
        random_piece = random.choice(possible_pieces)
        neighbour_bee = Bee(position=(random_piece.row, random_piece.col), cost=len(possible_pieces), board=bee.board)
        neighbour_bee.move(value=random_piece.number)
        return neighbour_bee
    return None


def evalute_bees(bees: List[Bee], bees_amount: int) -> List[Bee] | None:
    for bee in bees:
        if bee is None:
            return None
    sorted_bees = sorted(bees, key=lambda bee: bee.cost)
    return sorted_bees if len(bees) <= bees_amount else sorted_bees[:bees_amount]

def move_bee(bee: Bee, move_amount: int) -> Bee | None:
    moved_bee = bee
    for _ in range(move_amount):
        bee_neighbour = create_neighbour(bee=bee)
        if not bee_neighbour:
            return None
        if bee_neighbour.cost < bee.cost:
            moved_bee = deepcopy(bee_neighbour)
    return moved_bee


def bees_algorithm(board: Board, game: Game, max_iterations: int, population_size: int, bee_moves: int) -> Board | None:
    bees = [initialize_random_bee(board=board, game=game) for _ in range(population_size)]
    if not bees:
        return None

    best_bees = evalute_bees(bees=bees, bees_amount=5)
    employed_bees = [bee for bee in bees if bee not in best_bees]

    employed_bees_amount = len(employed_bees) // len(best_bees)
    
    best_bee = best_bees[0]
    for _ in range(max_iterations):
        if not bees:
            break
        best_bees = evalute_bees(bees=bees, bees_amount=5)
        if not best_bees:
            break
        employed_bees = [bee for bee in bees if bee not in best_bees]

        for idx, bee in enumerate(best_bees):
            bee = move_bee(bee=bee, move_amount=bee_moves)
            if not bee:
                break
            if best_bee.cost > bee.cost:
                best_bee = bee

            for i in range(employed_bees_amount):
                employed_bee = employed_bees[idx + i]
                move_bee(bee=employed_bee, move_amount=bee_moves)
                if best_bee.cost > bee.cost:
                    best_bee = bee

    return best_bee.board


if __name__ == "__main__":
    pygame.font.init()
    number_font = pygame.font.SysFont(None, 25)
