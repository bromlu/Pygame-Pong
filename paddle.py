import math

import contextlib
with contextlib.redirect_stdout(None): import pygame

class Paddle:
    def __init__(self, x, y, height, screen_width, screen_height, update_function):
        self.height = height
        self.color = pygame.Color(255, 255, 255, 255)
        self.blink_countdown = 0
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.rect = pygame.Rect(x, y, 10, height)
        self.update_function = update_function
        self.power = None

    def get_x(self):
        return self.rect.x

    def get_y(self):
        return self.rect.y

    def get_center_x(self):
        return self.rect.x + 5

    def get_center_y(self):
        return self.rect.y + self.height/2

    def set_x(self, new_x):
        self.rect.x = new_x

    def set_y(self, new_y):
        self.rect.y = new_y

    def set_power(self, power):
        if self.power is not None:
            return -1
        else:
            self.power = power
        return 0

    def grow(self):
        self.color = pygame.color.Color('green')
        self.blink_countdown = 10
        self.height += 10
        if self.height > self.screen_height/2:
            self.height = self.screen_height/2
        self.rect = pygame.Rect(self.get_x(), self.get_y(), 10, self.height)

    def shrink(self):
        self.color = pygame.color.Color('red')
        self.blink_countdown = 10
        self.height -= 10
        if self.height < 10:
            self.height = 10
        self.rect = pygame.Rect(self.get_x(), self.get_y(), 10, self.height)

    def draw(self, surface):
        color = self.color
        self.blink_countdown -= 1
        if self.blink_countdown <= 0:
            color = pygame.Color(255, 255, 255, 255)
        if self.power is not None:
            color = self.power.get_color()
        pygame.draw.rect(surface, color, self.rect)

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

    def use_power(self):
        if self.power is not None:
            self.power.use(self)
        self.power = None