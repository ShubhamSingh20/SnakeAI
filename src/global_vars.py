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
    HIDDEN_UNITS = (32, 16)
    NETWORK_LR = 0.01
    BATCH_SIZE = 64
    UPDATE_EVERY = 5
    GAMMA = 0.95
    epsilon, eps_min, eps_decay = 1, 0.05, 0.9997
    NUM_EPISODES = 10000    #number of episodes to train