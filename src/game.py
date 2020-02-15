from snake import Snake
from global_vars import Color, Screen, Segment
import pygame

# Set initial speed
x_change = Segment.DIFF
y_change = 0
 
# Call this function so the Pygame library can initialize itself
pygame.init()
 
# Create an 800x600 sized screen
screen = pygame.display.set_mode([
    Screen.SCREEN_WIDTH, Screen.SCREEN_HEIGTH
])
 
# Set the title of the window
pygame.display.set_caption('Snake AI')
myfont = pygame.font.SysFont("times new roman", 24)

snake = Snake()
 
snake.intial_movement()
snake.create_fruit()

clock = pygame.time.Clock()

done = False
 
while not done:
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and snake.direction != "right":
                snake.direction = "left"
                x_change = Segment.DIFF * -1
                y_change = 0
            if event.key == pygame.K_RIGHT and snake.direction != "left":
                snake.direction = "right"
                x_change = Segment.DIFF
                y_change = 0
            if event.key == pygame.K_UP and snake.direction != "down":
                snake.direction = "up"
                x_change = 0
                y_change = Segment.DIFF * -1
            if event.key == pygame.K_DOWN and snake.direction != "up":
                snake.direction = "down"
                x_change = 0
                y_change = Segment.DIFF

    snake.remove_old_segment()
    snake.insert_new_segment(x_change, y_change)

    if snake.check_collision():
        print("")

    if snake.ate_fruit():
        snake.give_point()
        snake.insert_new_segment(x_change, y_change)
    
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
        "Highest Score: {0}".format(snake.highest_score), True, Color.DARKGREEN
    )
    highest_score_rect = highest_score_surface.get_rect(topleft=(500, 10))
    screen.blit(highest_score_surface, highest_score_rect)

    clock.tick(20) # Framerate
 
pygame.quit()