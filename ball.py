import contextlib
with contextlib.redirect_stdout(None): import pygame

class Ball:
    def __init__(self, screen_width, screen_height, size, speed):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.size = size
        self.speed = speed
        self.rect = self.new_ball()

    def get_x(self):
        return self.rect.x

    def get_y(self):
        return self.rect.y

    def set_x(self, new_x):
        self.rect.x = new_x

    def set_y(self, new_y):
        self.rect.y = new_y

    def new_ball(self):
        self.vx = -5
        self.vy = 0
        return pygame.Rect(self.screen_width/2, self.screen_height/2, self.size, self.size)

    def draw(self, surface):
        pygame.draw.rect(surface, pygame.Color(255, 255, 255, 255), self.rect)

    def update(self, paddles):
        self.rect.x += self.vx
        self.rect.y += self.vy

        self.handle_paddle_collision(paddles)
        self.handle_bounds_collision()

    def handle_paddle_collision(self, paddles):
        index = self.rect.collidelist(paddles)
        if index != -1:
            self.vx, self.vy = paddles[index].bounce(self.rect.y + self.size/2, self.speed)

    def handle_bounds_collision(self):
        if self.rect.y >= self.screen_height - 10:
            self.vy = -1 * abs(self.vy)
        elif self.rect.y <= 0:
            self.vy = abs(self.vy)
        if self.rect.x >= self.screen_width - 10 or self.rect.x <= 0:
            self.rect = self.new_ball()
