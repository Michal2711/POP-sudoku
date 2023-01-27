import random
from copy import deepcopy
import pygame
import random
from typing import List, Tuple

from ..board import Sudoku
from ..game import Game

"""
initialize randomly scout bees;
while sudoku is not solved:
    evaluate bees cells; //from heuristic function
    select bees with high fitnesses;
    go to selected bees cells;
    search through selected bees cells with remaining bees;
"""

class Bee():
    def __init__(self, position: Tuple[int], cost: int, board: Sudoku) -> None:
        self.position = position
        self.cost = cost
        self.board = deepcopy(board)

    def move(self, value):
        self.board.move(row=self.position(0), col=self.position(1), number=value)


def initialize_random_bee(board: Board, game: Game) -> List[Bee]:
    cost = board.get_all_empty_pieces()
    possible_pieces = board.get_possibile_pieces(sudoku_size)
    random_piece = random.choice(possible_pieces)
    random_bee = Bee(position=(random_piece.row, random_piece.col), cost=len(possible_pieces), board=board)
    random_bee.move(value=random_piece.value)
    return random_bee


def create_neighbour(bee: Bee) -> Bee:
    possible_pieces = self.board.get_possibile_pieces()
    random_piece = random.choice(possible_pieces)
    neighbour_bee = Bee(position=(random_piece.row, random_piece.col), cost=len(possible_pieces), board=board)
    neighbour_bee.move(value=random_piece.value)
    return neighbour_bee


def evalute_bees(bees: List[Bee], bees_amount: int) -> List[Bee]:
    sorted_bees = sort(bees, lambda bee: bee.cost)
    return sorted_bees if len(bees) <= bees_amount else sorted_bees[bees_amount]


def bees_algorithm(board: Sudoku, game: Game, max_iterations: int, population_size: int) -> bool:
    min_poss = 9
    empty_pieces = board.get_all_empty_pieces()

    #INITIALIZE RANDOM BEES 
    bees = [initialize_random_bee(board=board, game=game) for _ in range(population_size)]

    # EVALUATE BEES
    best_bees = evalute_bees(bees=bees_init, bees_amount=5)
    employed_bees = [bee for bee in bees if bee not in best_bees]

    #EQUALL EMPLOYED BEES SPREAD AMOUNT
    employed_bees_amount = len(employed_bees) // len(best_bees)
    
    best_bee = best_bees[0]

    for _ in range(max_iterations):
        for bee in best_bees:

            bee_neighbour = create_neighbour(bee=bee)
            if bee_neighbour.cost < bee.cost:
                bee = deepcopy(bee_neighbour)
        
            if best_bee.cost > bee.cost:
                best_bee = bee

            for _ in range(employed_bees_amount):
                employed_bee = employed_bees.pop(0)

                bee_neighbour = create_neighbour(bee=employed_bee)
                if bee_neighbour.cost < bee.cost:
                    bee = deepcopy(bee_neighbour)
        
                if best_bee.cost > bee.cost:
                    best_bee = bee

    return best_bee


if __name__ == "__main__":
    pygame.font.init()
    number_font = pygame.font.SysFont(None, 25)
