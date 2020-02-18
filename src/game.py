from utils import (
    setup_game, update_score_text, 
    update_epoch_text, update_highest_score_text
)
from snake import Snake
from global_vars import *
import pygame
import time


def play_game_by_user():
    screen, myfont = setup_game()
    done, epoch, highest_score = False, 0, 0
    start_ticks = pygame.time.get_ticks()

    while not done:
        snake = Snake()
        x_change, y_change = Segment.DIFF, 0
        clock = pygame.time.Clock()
        snake.create_fruit()
        snake.intial_movement()
        snake_is_alive = True
        epoch += 1

        while snake_is_alive and not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and snake.direction != "right":
                        snake.move('left')

                    elif event.key == pygame.K_RIGHT and snake.direction != "left":
                        snake.move('right')

                    elif event.key == pygame.K_UP and snake.direction != "down":
                        snake.move('up')

                    elif event.key == pygame.K_DOWN and snake.direction != "up":
                        snake.move('down')
            else:
                # continue previous movement if no event is provided
                snake.move()

            if not snake.is_alive():
                snake_is_alive = False

            if snake.ate_fruit():
                snake.give_point(change_fruit=True)
                snake.insert_new_segment()
                
                if snake.score > highest_score:
                    highest_score = snake.score

            screen.fill(Color.BLACK)

            # Draw snake over black canvas
            snake.draw(screen)

            update_score_text(
                screen, myfont, "Score: {0}".format(snake.score)
            )
            update_highest_score_text(
                screen, myfont,
                "Highest Score: {0}".format(highest_score)
            )

            run_time = (pygame.time.get_ticks()-start_ticks) / 1000
            run_time = time.strftime("%M min:%S sec", time.gmtime(run_time)) 

            update_epoch_text(
                screen, myfont,
                "Training Epoch: {0} ({1})".format(epoch,  run_time)
            )

            pygame.display.flip()
            clock.tick(20) # Framerate

        del snake.allspriteslist, snake.fruit, snake

        pygame.time.delay(850)

    pygame.time.delay(400)
    pygame.quit()