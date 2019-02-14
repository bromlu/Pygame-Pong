import random
import math

import contextlib
with contextlib.redirect_stdout(None): import pygame

BOUNCE = pygame.mixer.Sound("assets/sfx_damage_hit1.wav")
SCORE = pygame.mixer.Sound("assets/sfx_sounds_error7.wav")

class Ball:
    def __init__(self, screen_width, screen_height, size, speed):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.size = size
        self.speed = speed
        self.rect = self.new_ball()
        self.score_left = False
        self.score_right = False

    def get_x(self):
        return self.rect.x

    def get_y(self):
        return self.rect.y

    def get_score_left(self):
        if(self.score_left):
            self.score_left = False
            return True
        return False

    def get_score_right(self):
        if(self.score_right):
            self.score_right = False
            return True
        return False

    def set_x(self, new_x):
        self.rect.x = new_x

    def set_y(self, new_y):
        self.rect.y = new_y

    def new_ball(self):
        self.vx = 0
        while(self.vx < 2 and self.vx > -2):
            angle = random.uniform(0, 2 * math.pi)
            self.vx = math.cos(angle) * self.speed
            self.vy = math.sin(angle) * self.speed
        x = self.screen_width/2 - self.size/2
        y = random.randint(0,self.screen_height - self.size)
        return pygame.Rect(x, y, self.size, self.size)

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
            BOUNCE.play()
            self.vx, self.vy = paddles[index].bounce(self.rect.y + self.size/2, self.speed)

    def handle_bounds_collision(self):
        if self.rect.y >= self.screen_height - 10:
            BOUNCE.play()
            self.vy = -1 * abs(self.vy)
        elif self.rect.y <= 0:
            BOUNCE.play()
            self.vy = abs(self.vy)
        if self.rect.x >= self.screen_width - 10:
            SCORE.play()
            self.score_right = True
            self.rect = self.new_ball()
        if self.rect.x <= 0:
            SCORE.play()
            self.score_left = True
            self.rect = self.new_ball()