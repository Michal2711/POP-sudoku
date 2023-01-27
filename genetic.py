from board import Board
import numpy as np
from piece import Piece
from math import factorial as fact
import random
import time

from copy import deepcopy

numbers = {'1': '1', '2': '2', '3': '3',
           '4': '4', '5': '5', '6': '6',
           '7': '7', '8': '8', '9': '9'}

CROSS_CHANCE = 0.4
MUTATION_CHANCE = 0.2
POPULATION_SIZE = 1000


def flatten_board(board: np.array):
    sudoku = []
    data = board.flatten()
    data = np.split(data, 27)
    for i in range(9, 27+1, 9):
        sudoku.append(np.stack(data[i-9:i:3]).flatten())
        sudoku.append(np.stack(data[i-9+1:i:3]).flatten())
        sudoku.append(np.stack(data[i-9+2:i:3]).flatten())
    sudoku = np.stack(sudoku)
    return sudoku


def unflatten_board(board: np.array):
    result = []
    for i in range(len(board)):
        result.append(np.split(board[i], 3))
    result = np.stack(result).reshape((27, 3))
    sudoku = []
    for i in range(9, 27+1, 9):
        sudoku.append(np.stack(result[i-9:i:3]).flatten())
        sudoku.append(np.stack(result[i-9+1:i:3]).flatten())
        sudoku.append(np.stack(result[i-9+2:i:3]).flatten())
    sudoku = np.stack(sudoku)
    return sudoku


def fill_in_board(board: np.array):
    result = deepcopy(board)
    for i in range(len(result)):
        non_zeros = np.nonzero(result[i])
        numbers_grid = numbers.copy()
        for elem in non_zeros[0]:
            numbers_grid.pop(str(int(result[i][elem])))
        for j in range(len(result[i])):
            if result[i][j] == 0:
                choice = random.choice(list(numbers_grid.values()))
                result[i][j] = int(choice)
                numbers_grid.pop(choice)
    return result


def calculate_sum(board: np.array):
    sum_rows = 0
    sum_col = 0
    for row in board:
        sum_rows += np.abs(45 - np.sum(row))
    for col in board.T:
        sum_col += np.abs(45 - np.sum(col))
    return sum_rows + sum_col


def calculate_product(board):
    prod_rows = 0
    prod_col = 0
    for row in board:
        prod_rows += np.abs(fact(9) - np.prod(row))
    for col in board.T:
        prod_col += np.abs(fact(9) - np.prod(col))
    return prod_col + prod_rows


def calculate_missing(board):
    count_rows = 0
    count_col = 0
    for row in board:
        for key in numbers.keys():
            if int(key) not in row:
                count_rows += 1
    for col in board.T:
        for key in numbers.keys():
            if int(key) not in col:
                count_col += 1
    return count_col + count_rows


def calculate_cost(board):
    cost = 0
    cost += 10*calculate_sum(board)
    cost += calculate_product(board)
    cost += 50*calculate_missing(board)
    return cost


def tournament(pop_len, scores, size_tournament):
    tournament = random.sample(range(pop_len), size_tournament)
    best_ix = tournament[0]
    for elem_ix in tournament:
        if scores[elem_ix] < scores[best_ix]:
            best_ix = elem_ix

    return best_ix


def uniform_cross(parent1, parent2):
    child1 = np.zeros((9, 9))
    child2 = np.zeros((9, 9))
    for idx in range(len(parent1)):
        if random.random() < CROSS_CHANCE:
            child1[idx] = parent1[idx]
            child2[idx] = parent2[idx]
        else:
            child1[idx] = parent2[idx]
            child2[idx] = parent1[idx]
    return child1, child2


def crossover(population):
    result = np.zeros((len(population), 9, 9))
    for idx in range(0, len(population), 2):
        first, second = uniform_cross(population[idx], population[idx+1])
        result[idx] = first
        result[idx+1] = second
    return result


def evaluate(population):
    scores = []
    for i in range(len(population)):
        scores.append(calculate_cost(unflatten_board(population[i])))
    return scores


def get_indexes(i, j, help_array):
    while True:
        idx1 = random.randint(0, 8)
        idx2 = random.randint(0, 8)
        if help_array[j][idx1] == 0 and help_array[j][idx2] == 0:
            return idx1, idx2


def mutation_swap(grid, i, j, help_array):
    new_grid = deepcopy(grid)
    idx1, idx2 = get_indexes(i, j, help_array)
    temp = new_grid[idx1]
    new_grid[idx1] = grid[idx2]
    new_grid[idx2] = temp
    return new_grid


def mutation(population, help_array):
    for i in range(len(population)):
        for j in range(len(population[i])):
            if random.random() < MUTATION_CHANCE:
                population[i][j] = mutation_swap(
                    population[i][j], i, j, help_array)
    return population


def selection(population, scores, size_tournament):
    children = []
    pop_len = len(population)
    for _ in range(pop_len):
        idx = tournament(pop_len, scores, size_tournament)
        children.append(population[idx])
    return children


def genetic_algorithm(board: Board):
    data = np.zeros((9, 9))
    piece: Piece
    for piece in board.get_all_pieces():
        data[piece.row][piece.col] = piece.number

    data = flatten_board(data)
    help_array = deepcopy(data)

    population = []
    for _ in range(POPULATION_SIZE):
        population.append(fill_in_board(data))

    scores = []
    t = 1000
    start_time = time.time()
    for i in range(t):
        # children = []
        scores = evaluate(population)
        population = selection(population, scores, 30)
        population = crossover(population)
        population = mutation(population, help_array)
        print(f"Cost function: {np.min(scores)}")
        if 0.0 in scores:
            result = np.argmin(scores)
            print("Succes!")
            result = unflatten_board(population[result].astype(int))
            break
    end_time = time.time() - start_time

    print(f"Time working: {end_time: .2f} seconds")

    for i in range(len(result)):
        for j in range(len(result[i])):
            board.move(i, j, result[i][j])

    return board
