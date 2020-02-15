from snake import Snake
from global_vars import Color, Screen, Segment
import pygame

# Set initial speed
x_change = Segment.SEGMENT_WDITH + Segment.SEGMENT_MARGIN
y_change = 0
 
# Call this function so the Pygame library can initialize itself
pygame.init()
 
# Create an 800x600 sized screen
screen = pygame.display.set_mode([
    Screen.SCREEN_WIDTH, Screen.SCREEN_HEIGTH
])
 
# Set the title of the window
pygame.display.set_caption('Snake AI')

snake = Snake()
 
snake.intial_movement()
snake.create_fruit()

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
            if event.key == pygame.K_LEFT and snake.direction != "right":
                snake.direction = "left"
                x_change = (Segment.SEGMENT_WDITH + Segment.SEGMENT_MARGIN) * -1
                y_change = 0
            if event.key == pygame.K_RIGHT and snake.direction != "left":
                snake.direction = "right"
                x_change = (Segment.SEGMENT_WDITH + Segment.SEGMENT_MARGIN)
                y_change = 0
            if event.key == pygame.K_UP and snake.direction != "down":
                snake.direction = "up"
                x_change = 0
                y_change = (Segment.SEGMENT_HEIGHT + Segment.SEGMENT_MARGIN) * -1
            if event.key == pygame.K_DOWN and snake.direction != "up":
                snake.direction = "down"
                x_change = 0
                y_change = (Segment.SEGMENT_HEIGHT + Segment.SEGMENT_MARGIN)

    snake.remove_old_segment()
    snake.insert_new_segment(x_change, y_change)
    print(snake.check_collision())
    
    screen.fill(Color.BLACK)
    snake.draw(screen)
    pygame.display.flip()
    clock.tick(20) # Framerate
 
pygame.quit()