from snake import Snake
from global_vars import Color, Screen, SegmentGlobal
import pygame

# Set initial speed
x_change = SegmentGlobal.SEGMENT_WDITH + SegmentGlobal.SEGMENT_MARGIN
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
                snake.direction = "left"
                x_change = (SegmentGlobal.SEGMENT_WDITH + SegmentGlobal.SEGMENT_MARGIN) * -1
                y_change = 0
            if event.key == pygame.K_RIGHT:
                snake.direction = "right"
                x_change = (SegmentGlobal.SEGMENT_WDITH + SegmentGlobal.SEGMENT_MARGIN)
                y_change = 0
            if event.key == pygame.K_UP:
                snake.direction = "up"
                x_change = 0
                y_change = (SegmentGlobal.SEGMENT_HEIGHT + SegmentGlobal.SEGMENT_MARGIN) * -1
            if event.key == pygame.K_DOWN:
                snake.direction = "down"
                x_change = 0
                y_change = (SegmentGlobal.SEGMENT_HEIGHT + SegmentGlobal.SEGMENT_MARGIN)
 
    

    snake.remove_old_segment()
    snake.insert_new_segment(x_change, y_change)
    print(snake.check_collision())
    
    screen.fill(Color.BLACK)
    snake.draw(screen)
    pygame.display.flip()
    clock.tick(20) # Framerate
 
pygame.quit()