from utils import (
    setup_game, update_score_text, 
    update_epoch_text, update_highest_score_text
)
from global_vars import (
    GENETIC, Segment
)
from snake import Snake
import pygame

def computer_play():
    screen, myFont = setup_game()
    done, epoch, highest_score = False, 0, 0
    total_games_to_play = 1
    start_ticks = pygame.time.get_ticks()

    for _ in range(total_games_to_play):
        snake = Snake()
        x_change, y_change = Segment.DIFF, 0
        clock = pygame.time.Clock()
        snake.create_fruit()
        snake.intial_movement()
        snake_is_alive = True
        epoch += 1

        for __ in range(GENETIC.STEPS_PER_GAME):
            pass