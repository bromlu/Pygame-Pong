import math
import contextlib
with contextlib.redirect_stdout(None): import pygame

class Paddle:
    def __init__(self, x, y, height, screen_width, screen_height, update_function):
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.rect = pygame.Rect(x, y, 10, height)
        self.update_function = update_function

    def get_x(self):
        return self.rect.x

    def get_y(self):
        return self.rect.y

    def set_x(self, new_x):
        self.rect.x = new_x

    def set_y(self, new_y):
        self.rect.y = new_y

    def draw(self, surface):
        pygame.draw.rect(surface, pygame.Color(255, 255, 255, 255), self.rect)

    def update(self, keys_pressed, ball_x, ball_y):
        self.update_function(self, keys_pressed, ball_x, ball_y)

    def bounce(self, y, speed):
        relative_intersect_y = (self.get_y() + (self.height/2)) - y
        normalized_intersect_y = relative_intersect_y/(self.height/2)
        angle = normalized_intersect_y * (4*math.pi/12)

        if self.get_x() <= self.screen_width/2:
            new_vx = speed * math.cos(angle)
            new_vy = speed * -math.sin(angle)
        else:
            new_vx = speed * -math.cos(angle)
            new_vy = speed * -math.sin(angle)

        return new_vx, new_vy