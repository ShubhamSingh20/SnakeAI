from snake import Snake
from global_vars import (
    Color, Screen, Segment, COMPUTER_TRAIN, Q_LEARN
)
from qlearning import get_q_table
import numpy as np
import pygame
import time


def perc_heigth(perc):
    return (Screen.SCREEN_HEIGTH * perc/100)

def perc_width(perc):
    return (Screen.SCREEN_WIDTH * perc/100)

q_table = get_q_table()

pygame.init()

screen = pygame.display.set_mode([
    Screen.SCREEN_WIDTH, Screen.SCREEN_HEIGTH
])

pygame.display.set_caption('Snake AI')
myfont = pygame.font.SysFont("times new roman", 24)
done, epoch, highest_score = False, 0, 0

start_ticks = pygame.time.get_ticks()
episode_rewards = []

action_direction = {
    0: pygame.K_UP,
    1: pygame.K_DOWN,
    2: pygame.K_RIGHT,
    3: pygame.K_LEFT,
}

while not done:
    snake = Snake()
    x_change, y_change = Segment.DIFF, 0
    clock = pygame.time.Clock()
    snake.create_fruit()
    snake.intial_movement()
    snake_is_alive = True
    epoch += 1

    episode_reward = 0

    while snake_is_alive and not done:
        if COMPUTER_TRAIN:
            observation = (snake.get_dist_fruit())
            if np.random.random() > Q_LEARN.EPSILON:
                action = np.argmax(q_table[observation])
                action = action_direction[action]
            else:
                action = np.random.randint(pygame.K_UP, pygame.K_LEFT + 1)

            if action == pygame.K_LEFT and snake.direction != "right":
                snake.direction = "left"
                x_change, y_change = Segment.DIFF * -1, 0
                snake.move(x_change, y_change)

            elif action == pygame.K_RIGHT and snake.direction != "left":
                snake.direction = "right"
                x_change, y_change = Segment.DIFF, 0
                snake.move(x_change, y_change)

            elif action == pygame.K_UP and snake.direction != "down":
                snake.direction = "up"
                x_change, y_change = 0, Segment.DIFF * -1
                snake.move(x_change, y_change)

            elif action == pygame.K_DOWN and snake.direction != "up":
                snake.direction = "down"
                x_change, y_change = 0, Segment.DIFF
                snake.move(x_change, y_change)

            if not snake.is_alive():
                reward = -Q_LEARN.DEATH_PENALTY
            elif snake.ate_fruit():
                reward = Q_LEARN.FOOD_REWARD
            else:
                reward = -Q_LEARN.MOVE_PENALTY
            
            new_observation = (snake.get_dist_fruit())
            max_future_q = np.max(q_table[new_observation])

            current_q = q_table[observation][pygame.K_LEFT - action]

            if reward == Q_LEARN.FOOD_REWARD:
                new_q = Q_LEARN.FOOD_REWARD
            elif reward == -Q_LEARN.DEATH_PENALTY:
                new_q = -Q_LEARN.DEATH_PENALTY
            else:
                new_q = (1 - Q_LEARN.LEARNING_RATE) * current_q \
                    + Q_LEARN.LEARNING_RATE * (reward + Q_LEARN.DISCOUNT * max_future_q)

                q_table[observation][pygame.K_LEFT - action] = new_q
            
            episode_reward += reward
            episode_rewards.append(episode_reward)
            Q_LEARN.EPSILON *= Q_LEARN.EPS_DECAY

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and snake.direction != "right":
                        snake.direction = "left"
                        x_change, y_change = Segment.DIFF * -1, 0
                        snake.move(x_change, y_change)

                    elif event.key == pygame.K_RIGHT and snake.direction != "left":
                        snake.direction = "right"
                        x_change, y_change = Segment.DIFF, 0
                        snake.move(x_change, y_change)

                    elif event.key == pygame.K_UP and snake.direction != "down":
                        snake.direction = "up"
                        x_change, y_change = 0, Segment.DIFF * -1
                        snake.move(x_change, y_change)

                    elif event.key == pygame.K_DOWN and snake.direction != "up":
                        snake.direction = "down"
                        x_change, y_change = 0, Segment.DIFF
                        snake.move(x_change, y_change)
            else:
                # continue previous movement if no event is provided
                snake.move(x_change, y_change)

        if not snake.is_alive():
            snake_is_alive = True

        if snake.ate_fruit():
            snake.give_point(change_fruit=False)
            snake.insert_new_segment(x_change, y_change)
            
            if snake.score > highest_score:
                highest_score = snake.score

        screen.fill(Color.BLACK)

        # Draw snake over black canvas
        snake.draw(screen)

        # Score Text
        score_surface = myfont.render(
            "Score: {0}".format(snake.score), True, Color.DARKGREEN
        )
        score_rect = score_surface.get_rect(topleft=(perc_width(3), perc_heigth(1)))
        screen.blit(score_surface, score_rect)

        # Highest Score Text
        highest_score_surface = myfont.render(
            "Highest Score: {0}".format(highest_score), True, Color.DARKGREEN
        )

        highest_score_rect = highest_score_surface.get_rect(topleft=(perc_width(65), perc_heigth(1)))
        screen.blit(highest_score_surface, highest_score_rect)

        # EPoch Text and Trainging time
        run_time = (pygame.time.get_ticks()-start_ticks) / 1000
        run_time = time.strftime("%M min:%S sec", time.gmtime(run_time)) 

        epoch_surface = myfont.render(
            "Training Epoch: {0} ({1})" \
                .format(epoch,  run_time), 
                True, Color.YELLOW
        )

        epoch_rect = epoch_surface.get_rect(bottomleft=(perc_width(20), perc_heigth(98)))
        screen.blit(epoch_surface, epoch_rect)

        pygame.display.flip()
        clock.tick(20) # Framerate

    del snake.allspriteslist, snake.fruit, snake
    
    pygame.time.delay(850)

pygame.time.delay(400)
pygame.quit()