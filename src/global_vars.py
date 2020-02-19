"""
>>> pygame.K_UP
273
>>> pygame.K_DOWN
274
>>> pygame.K_RIGHT
275
>>> pygame.K_LEFT
276
"""

COMPUTER_TRAIN = True

class GENETIC:
    n_x = 7 # inputs like direction of fruit, snake and blocked
    n_h = 9
    n_h2 = 15
    n_y = 3 # where to move left, current, right

    SOL_PER_POP = 50
    NUM_WEIGHTS = (
        n_x* n_h + \
        n_h* n_h2 + \
        n_h2* n_y
    )
    STEPS_PER_GAME = 2500
    TESTS_PER_GAME = 1
    NUM_GEN = 100
    NUM_PARENT_MATING = 12 
    POPULATION_SIZE = (
        SOL_PER_POP, 
        NUM_WEIGHTS
    )


class Q_LEARN:
    ACTION_SIZE = 4
    HM_EPISODES = 25_000
    MOVE_PENALTY = 1
    FOOD_REWARD = 30
    DEATH_PENALTY = 300
    EPSILON = 0.9
    EPS_DECAY = 0.9998
    LEARNING_RATE = 0.1
    DISCOUNT = 0.95
    Q_TABLE_FILENAME = None


class Color:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    DARKGREEN = (0, 155, 0)
    YELLOW = (255, 255, 0)
    DARKGRAY  = (40, 40, 40)


class Segment:
    X_START = 300
    Y_START = 300
    SEGMENT_HEIGHT = 20
    SEGMENT_WDITH = 20
    DIFF = 15


class Screen:
    SCREEN_HEIGTH = 500 
    SCREEN_WIDTH = 500


class NeuralNetwork:
    n_x = 7
    n_h = 9
    n_h2 = 15
    n_y = 3
    W1_shape = (9,7)
    W2_shape = (15,9)
    W3_shape = (3,15)
