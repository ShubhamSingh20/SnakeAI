from snake import Snake
from global_vars import (
    Color, Screen, Segment, TRAIN
)
import pygame
import time

pygame.init()
 

screen = pygame.display.set_mode([
    Screen.SCREEN_WIDTH, Screen.SCREEN_HEIGTH
])

pygame.display.set_caption('Snake AI')
myfont = pygame.font.SysFont("times new roman", 24)
done = False
epoch = 0
highest_score = 0

start_ticks=pygame.time.get_ticks()

while not done:
    snake = Snake()
    x_change = Segment.DIFF
    y_change = 0
 
    clock = pygame.time.Clock()
    snake.create_fruit()
    snake.intial_movement()
    snake_is_alive = True
    epoch += 1

    while snake_is_alive and not done:
        if TRAIN:
            pass
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and snake.direction != "right":
                        snake.direction = "left"
                        snake.move(Segment.DIFF * -1, 0)

                    elif event.key == pygame.K_RIGHT and snake.direction != "left":
                        snake.direction = "right"
                        snake.move(Segment.DIFF, 0)

                    elif event.key == pygame.K_UP and snake.direction != "down":
                        snake.direction = "up"
                        snake.move(0, Segment.DIFF * -1)

                    elif event.key == pygame.K_DOWN and snake.direction != "up":
                        snake.direction = "down"
                        snake.move(0, Segment.DIFF)
            else:
                # continue previous movement if no event is provided
                snake.move(x_change, y_change)

        if not snake.is_alive():
            snake_is_alive = False

        if snake.ate_fruit():
            snake.give_point()
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
        score_rect = score_surface.get_rect(topleft=(10, 10))
        screen.blit(score_surface, score_rect)

        # Highest Score Text
        highest_score_surface = myfont.render(
            "Highest Score: {0}".format(highest_score), True, Color.DARKGREEN
        )
        highest_score_rect = highest_score_surface.get_rect(topleft=(500, 10))
        screen.blit(highest_score_surface, highest_score_rect)

        # EPoch Text and Trainging time
        run_time = (pygame.time.get_ticks()-start_ticks) / 1000
        run_time = time.strftime("%M min:%S sec", time.gmtime(run_time)) 

        epoch_surface = myfont.render(
            "Training Epoch: {0} ({1})" \
                .format(epoch,  run_time), 
                True, Color.YELLOW
        )
        epoch_rect = epoch_surface.get_rect(bottomleft=(200, 680))
        screen.blit(epoch_surface, epoch_rect)

        pygame.display.flip()
        clock.tick(20) # Framerate

    del snake.allspriteslist, snake.fruit, snake
    pygame.time.delay(850)

pygame.time.delay(400)
pygame.quit()