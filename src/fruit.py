import pygame
from global_vars import Segment, Color

class FruitSegment(pygame.sprite.Sprite):
    def __init__(self, x, y):
        # Call the parent's constructor
        super().__init__()
        # Set height, width
        self.image = pygame.Surface([
            Segment.SEGMENT_HEIGHT, Segment.SEGMENT_WDITH
        ])
        self.image.fill(Color.RED)
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Fruit(object):
    pass