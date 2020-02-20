from fruit import Fruit
from global_vars import (
    Color, Segment, Screen
)
import numpy as np
import pygame
import math


class SnakeSegment(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([
            Segment.SEGMENT_HEIGHT, Segment.SEGMENT_WDITH
        ])
        self.image.fill(Color.WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Snake(object):

    def __init__(self):
        self.score = 0
        self.fruit = None
        self.snake_len = 5
        self.y_change = 0
        self.x_change = Segment.DIFF
        self.direction = "right"
        self.snake_segments = []
        self.allspriteslist = pygame.sprite.Group()
    
    def get_position(self):
        cor = [[seg.rect.x, seg.rect.y] for seg in self.snake_segments]
        return cor

    def get_head_position(self):
        cor = self.snake_segments[0].rect
        return [cor.x, cor.y]
    
    def get_fruit_distance(self):
        return np.linalg.norm(
            np.array(self.fruit.get_fruit_position()) - \
                np.array(self.get_head_position())
        )
    
    def get_relative_direction(self, relative_direction):

        if self.direction == 'left':
            if relative_direction == 'left':
                return 'up'

            if relative_direction == 'right':
                return 'down'

        if self.direction == 'right':
            if relative_direction == 'left':
                return 'down'

            if relative_direction == 'right':
                return 'up'
        
        if self.direction == 'up':
            if relative_direction == 'left':
                return 'left'

            if relative_direction == 'right':
                return 'right'
        
        if self.direction == 'down':
            if relative_direction == 'left':
                return 'right'

            if relative_direction == 'right':
                return 'left'

    def get_angle_with_fruit(self):
        fruit_direction_vector = np.array(self.fruit.get_fruit_position()) \
            - np.array(self.get_head_position())
        
        snake_pos = self.get_position()
        snake_direction_vector = np.array(snake_pos[0]) - np.array(snake_pos[1])

        norm_of_fruit_direction_vector = np.linalg.norm(fruit_direction_vector)
        norm_of_snake_direction_vector = np.linalg.norm(snake_direction_vector)

        if norm_of_fruit_direction_vector == 0:
            norm_of_fruit_direction_vector = 10

        if norm_of_snake_direction_vector == 0:
            norm_of_snake_direction_vector = 10
        
        fruit_direction_vector_normalized = fruit_direction_vector / \
            norm_of_fruit_direction_vector

        snake_direction_vector_normalized = snake_direction_vector / \
            norm_of_snake_direction_vector

        angle = math.atan2(
            fruit_direction_vector_normalized[1] * snake_direction_vector_normalized[0] \
                - fruit_direction_vector_normalized[0] * snake_direction_vector_normalized[1],
            
            fruit_direction_vector_normalized[1] * snake_direction_vector_normalized[1] + \
                fruit_direction_vector_normalized[0] * snake_direction_vector_normalized[0]
        )

        angle = angle / math.pi

        return (
            angle, snake_direction_vector, fruit_direction_vector_normalized, 
            snake_direction_vector_normalized
        )

    def create_fruit(self):
        x_cor = [seg.rect.x for seg in self.snake_segments]
        y_cor = [seg.rect.y for seg in self.snake_segments]
        self.fruit = Fruit(x_cor, y_cor)
        self.allspriteslist.add(self.fruit)
    
    def remove_fruit(self):
        self.allspriteslist.remove(self.fruit)
    
    def intial_movement(self):
        for i in range(self.snake_len):
            x = Segment.X_START - Segment.DIFF * i
            y = Segment.Y_START
            segment = SnakeSegment(x, y)
            self.snake_segments.append(segment)
            self.allspriteslist.add(segment)

    def draw(self, screen):
        self.allspriteslist.draw(screen)
    
    def remove_old_segment(self):
        old_segment = self.snake_segments.pop()
        self.allspriteslist.remove(old_segment)

    def insert_new_segment(self):
        x = self.snake_segments[0].rect.x + self.x_change
        y = self.snake_segments[0].rect.y + self.y_change
        segment = SnakeSegment(x, y)
        self.snake_segments.insert(0, segment)
        self.allspriteslist.add(segment)
    
    def move(self, direction=None):
        if direction is None:
            direction = self.direction

        if direction == 'left':
            self.direction = direction
            self.x_change, self.y_change = Segment.DIFF * -1, 0

        if direction == 'right':
            self.direction = direction
            self.x_change, self.y_change = Segment.DIFF, 0
        
        if direction == 'up':
            self.direction = direction
            self.x_change, self.y_change = 0, Segment.DIFF * -1
        
        if direction == 'down':
            self.direction = direction
            self.x_change, self.y_change = 0, Segment.DIFF
        
        self.remove_old_segment()
        self.insert_new_segment()

    def check_body_collision(self, snake_segments=None):
        if snake_segments is None:
            snake_segments = self.snake_segments
        snake_head = snake_segments[0]
        for i, seg in enumerate(snake_segments[1:]):
            if snake_head.rect.x == seg.rect.x and snake_head.rect.y == seg.rect.y:
                return True
        return False
    
    def check_boundry_collision(self, snake_segments=None):
        if snake_segments is None:
            snake_segments = self.snake_segments
        snake_head = snake_segments[0]
        return (
            abs(snake_head.rect.x) >= Screen.SCREEN_WIDTH or snake_head.rect.x <= 0 or \
            abs(snake_head.rect.y) >= Screen.SCREEN_HEIGTH or snake_head.rect.y <= 0
        )
   
    def check_collision(self, snake_segments=None):
        return (
            self.check_body_collision(snake_segments) or 
            self.check_boundry_collision(snake_segments)
        )

    def is_alive(self):
        return not self.check_collision()

    def ate_fruit(self):
        snake_head = self.snake_segments[0]
        return (
            snake_head.rect.x == self.fruit.rect.x and \
            snake_head.rect.y == self.fruit.rect.y
        )
    
    def give_point(self, change_fruit=True):
        self.score += 1
        self.snake_len += 1

        if change_fruit:
            # new fruit on new location
            self.remove_fruit()
            self.create_fruit()

    def get_dist_fruit(self):
        snake_head = self.snake_segments[0]
        dist = (snake_head.rect.x - self.fruit.rect.x)**2 + \
            (snake_head.rect.y - self.fruit.rect.y)**2

        dist = math.sqrt(dist)
        return dist

    def soft_move(self, direction=None):
        """
            Doesn't actually move the snakes just returns the 
            next coordinates of snake head for a given move
        """
        x_change, y_change = 0, 0

        if direction is None:
            direction = self.direction

        if direction == 'left':
            x_change, y_change = Segment.DIFF * -1, 0

        if direction == 'right':
            x_change, y_change = Segment.DIFF, 0
        
        if direction == 'up':
            x_change, y_change = 0, Segment.DIFF * -1
        
        if direction == 'down':
            x_change, y_change = 0, Segment.DIFF
        
        temp_segment = self.get_position()

        # update head coordinates
        temp_segment[0] = [temp_segment[0][0] + x_change, temp_segment[0][1] + y_change] 

        temp_snake_segment = [
            SnakeSegment(i[0], i[1]) for i in  temp_segment 
        ]

        return temp_snake_segment
    
    def is_direction_blocked(self, direction):
        snake_segments = self.soft_move(direction)
        return self.check_collision(snake_segments)

    def blocked_directions_vector(self):
        """
            returns the vector in order [front, left, right]
        """
        return [
            self.is_direction_blocked(self.direction),
            self.is_direction_blocked(self.get_relative_direction('left')),
            self.is_direction_blocked(self.get_relative_direction('right')),
        ]

    