import math

import contextlib
with contextlib.redirect_stdout(None): import pygame

class Power:
    def __init__(self, x, y, size, screen_width, screen_height, vx, vy, color):
        self.vx = vx
        self.vy = vy
        self.rect = pygame.Rect(x, y, size, size)
        self.collected = False
        self.delete = False
        self.color = color

        self.screen_height = screen_height
        self.screen_width = screen_width

    def get_collected(self):
        return self.collected

    def get_delete(self):
        return self.delete

    def get_color(self):
        return self.color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def update(self, paddles):
        self.rect.x += self.vx
        self.rect.y += self.vy

        self.handle_paddle_collision(paddles)
        self.handle_bounds_collision()

    def handle_paddle_collision(self, paddles):
        index = self.rect.collidelist(paddles)
        if index != -1:
            result = paddles[index].set_power(self)
            if result == -1:
                self.delete = True
            self.collected = True

    def handle_bounds_collision(self):
        if self.rect.y >= self.screen_height - 10:
            self.vy = -1 * abs(self.vy)
        elif self.rect.y <= 0:
            self.vy = abs(self.vy)
        if self.rect.x >= self.screen_width - 10:
            self.delete = True
        if self.rect.x <= 0:
            self.delete = True

class Grow_Power(Power):
    def __init__(self, x, y, size, screen_width, screen_height, vx, vy):
        Power.__init__(self, x, y, size, screen_width, screen_height, vx, vy, pygame.color.Color('green'))

    def use(self, paddle):
        paddle.grow()

class Shrink_Power(Power):
    def __init__(self, x, y, size, screen_width, screen_height, vx, vy):
        Power.__init__(self, x, y, size, screen_width, screen_height, vx, vy, pygame.color.Color('red'))

    def use(self, paddle):
        self.originPaddle = paddle
        self.rect = pygame.Rect(paddle.get_center_x(), paddle.get_center_y(), 10, 2)
        self.vx = math.copysign(abs(self.vx) + abs(self.vy), -1 * self.vx)
        self.vy = 0
        self.collected = False
        self.handle_paddle_collision = self.handle_paddle_attack_collision

    def handle_paddle_attack_collision(self, paddles):
        index = self.rect.collidelist(paddles)
        if index != -1:
            if paddles[index] != self.originPaddle:
                paddles[index].shrink()
                self.delete = True
                self.collected = True