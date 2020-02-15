import pygame
from random import randrange
from global_vars import Segment, Color, Screen

class FruitSegment(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([
            Segment.SEGMENT_HEIGHT, Segment.SEGMENT_WDITH
        ])
        self.image.fill(Color.RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Fruit(FruitSegment):
    
    def get_random_not_in_list(self, cor_list, screen_res):
        while True:
            tmp = randrange(
                Segment.DIFF, 
                screen_res - Segment.DIFF * 2, Segment.DIFF
            )
            if tmp not in cor_list:
                return tmp

    def __init__(self, snake_x, snake_y):
        x = self.get_random_not_in_list(snake_x, Screen.SCREEN_WIDTH)
        y = self.get_random_not_in_list(snake_y, Screen.SCREEN_HEIGTH)
        super().__init__(x, y)