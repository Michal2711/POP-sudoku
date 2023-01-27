import random
from copy import deepcopy
import pygame
import random
from typing import List, Tuple

from utils.board import Board
from utils.game import Game


class Bee():
    def __init__(self, position: Tuple[int], cost: int, board: Board) -> None:
        self.position = position
        self.cost = cost
        self.board = deepcopy(board)

    def move(self, value: int) -> None:
        self.board.move(row=self.position[0], col=self.position[1], number=value)


def initialize_random_bee(board: Board) -> List[Bee] | None:
    possible_pieces = board.get_possibile_pieces()
    empty_pieces = board.get_all_empty_pieces()
    if possible_pieces:
        random_piece = random.choice(possible_pieces)
        random_bee = Bee(position=(random_piece.row, random_piece.col), cost=len(empty_pieces) * len(random_piece.valid_numbers), board=board)
        random_bee.move(value=random_piece.number)
        return random_bee
    return None


def create_neighbour(bee: Bee) -> Bee:
    possible_pieces = bee.board.get_possibile_pieces()
    empty_pieces = bee.board.get_all_empty_pieces()
    if possible_pieces:
        sorted_pieces = sorted(possible_pieces, key=lambda piece: abs(bee.position[0] - piece.row) + abs(bee.position[1] - piece.col))
        piece = sorted_pieces[0]
        
        neighbour_bee = Bee(position=(piece.row, piece.col), cost=len(empty_pieces) * len(piece.valid_numbers), board=bee.board)
        neighbour_bee.move(value=piece.number)
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


def bees_algorithm(board: Board, game: Game, max_iterations: int, population_size: int, bee_moves: int) -> Bee:
    best_bee = initialize_random_bee(board=board)
    while max_iterations and best_bee.cost != 0:
        max_iterations -= 1
        bees = [initialize_random_bee(board=board) for _ in range(population_size)]
        if not bees:
            break

        best_bees = evalute_bees(bees=bees, bees_amount=5)
        if not best_bees:
            break

        employed_bees = [bee for bee in bees if bee not in best_bees]

        employed_bees_amount = len(employed_bees) // len(best_bees)

        best_bees = evalute_bees(bees=bees, bees_amount=5)
        if not best_bees:
            break
        employed_bees = [bee for bee in bees if bee not in best_bees]

        for idx, bee in enumerate(best_bees):
            moved_bee = move_bee(bee=bee, move_amount=bee_moves)
            if not moved_bee:
                break
            if best_bee.cost > moved_bee.cost:
                best_bee = moved_bee

            for i in range(employed_bees_amount):
                employed_bee = employed_bees[idx + i]
                moved_bee = move_bee(bee=employed_bee, move_amount=bee_moves)
                if not moved_bee:
                    break
                if best_bee.cost > moved_bee.cost:
                    best_bee = moved_bee

        board = best_bee.board
        game.board = best_bee.board
        game.update()
        
    return best_bee
