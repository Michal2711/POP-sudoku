BASE = 3
ROWS, COLS = BASE*BASE, BASE*BASE
WIDTH, HEIGHT = BASE*200, BASE*200
# LEVEL_PARAM_1 < LEVEL_PARAM_2 !!!
# the quotient LEVEL_PARAM_1/LEVEL_PARAM_2 is greater but less than 1, the greater the level of difficulty
LEVEL_PARAM_1 = 70
LEVEL_PARAM_2 = 100

SQUARE_SIZE = WIDTH // COLS

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# ACO
ANT_STEP_RANGE = 4
NUMBER_OF_ANTS = 5


# BEES
BEES_AMOUNT = 10
BEES_MOVE = 2
MAX_ITER = 100

# testing
TEST_BOARD_NUMBER = 30
