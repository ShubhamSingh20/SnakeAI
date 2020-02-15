import pygame
from global_vars import (
    Color, SegmentGlobal, Screen
)

class Segment(pygame.sprite.Sprite):
    """ Class to represent one segment of the snake. """
    # -- Methods
    # Constructor function
    def __init__(self, x, y):
        # Call the parent's constructor
        super().__init__()
        # Set height, width
        self.image = pygame.Surface([
            SegmentGlobal.SEGMENT_HEIGHT, SegmentGlobal.SEGMENT_WDITH
        ])
        self.image.fill(Color.WHITE)
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Snake(object):

    def __init__(self):
        self.score = 0
        self.highest_score = 0
        self.snake_segments = []
        self.screen_wdith = Screen.SCREEN_WIDTH
        self.screen_height = Screen.SCREEN_HEIGTH
        self.allspriteslist = pygame.sprite.Group()
    
    def intial_movement(self):
        for i in range(15):
            x = 250 - (SegmentGlobal.SEGMENT_WDITH + SegmentGlobal.SEGMENT_MARGIN) * i
            y = 30
            segment = Segment(x, y)
            self.snake_segments.append(segment)
            self.allspriteslist.add(segment)

    def draw(self, screen):
        self.allspriteslist.draw(screen)
    
    def remove_old_segment(self):
        old_segment = self.snake_segments.pop()
        self.allspriteslist.remove(old_segment)

    def insert_new_segment(self, x_change, y_change):
        x = self.snake_segments[0].rect.x + x_change
        y = self.snake_segments[0].rect.y + y_change
        segment = Segment(x, y)
        self.snake_segments.insert(0, segment)
        self.allspriteslist.add(segment)
    
    def check_collision(self):
        snake_head = self.snake_segments[0]
        for seg in self.snake_segments[1:]:
            if snake_head.rect.colliderect(seg.rect):
                return True
        return False

 



        