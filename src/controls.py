from utils import (
    setup_game, update_score_text, 
    update_epoch_text, update_highest_score_text
)
from global_vars import (
    GENETIC, Segment
)
from snake import Snake
from genetic import TrainSnake
import pygame

def computer_play():
    trainsnake = TrainSnake()
    trainsnake.training_generation()