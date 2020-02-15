from snake import Snake
import pygame
 
# --- Globals ---
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
 
# Set the width and height of each snake segment
segment_width = 15
segment_height = 15
# Margin between each segment
segment_margin = 3
 
# Set initial speed
x_change = segment_width + segment_margin
y_change = 0
 
# Call this function so the Pygame library can initialize itself
pygame.init()
 
# Create an 800x600 sized screen
screen = pygame.display.set_mode([800, 600])
 
# Set the title of the window
pygame.display.set_caption('Snake AI')

snake = Snake()
 
snake.intial_movement()
 
clock = pygame.time.Clock()
done = False
 
while not done:
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
 
        # Set the speed based on the key pressed
        # We want the speed to be enough that we move a full
        # segment, plus the margin.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_change = (segment_width + segment_margin) * -1
                y_change = 0
            if event.key == pygame.K_RIGHT:
                x_change = (segment_width + segment_margin)
                y_change = 0
            if event.key == pygame.K_UP:
                x_change = 0
                y_change = (segment_height + segment_margin) * -1
            if event.key == pygame.K_DOWN:
                x_change = 0
                y_change = (segment_height + segment_margin)
 
    
    snake.remove_old_segment()
    snake.insert_new_segment(x_change, y_change)
    print(snake.check_collision())
    
    screen.fill(BLACK)
    snake.draw(screen)
    pygame.display.flip()
    clock.tick(20) # Framerate
 
pygame.quit()