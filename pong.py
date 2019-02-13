#!/usr/bin/python3

import os
import sys
import time

from ball import Ball
from paddle import Paddle
from text import Text
from players import manual_player_1, manual_player_2, AI_player

import contextlib
with contextlib.redirect_stdout(None): import pygame

WIDTH = 600
HEIGHT = 400
PADDLE_HEIGHT = 80
BALL_SIZE = 10
BALL_SPEED = 5

pygame.font.init()
pygame.display.set_caption('Pong')

screen = pygame.display.set_mode((WIDTH, HEIGHT))
surface= pygame.display.get_surface()

ball = Ball(WIDTH, HEIGHT, BALL_SIZE, BALL_SPEED)
paddles = [
    Paddle(550, 160, PADDLE_HEIGHT, WIDTH, HEIGHT, manual_player_1),
    Paddle(40, 160, PADDLE_HEIGHT, WIDTH, HEIGHT, manual_player_2)
]
left_score = "0"
right_score = "0"
left_score_text = Text(WIDTH/4, 50, left_score)
right_score_text = Text(WIDTH/4*3, 50, right_score)

clock = pygame.time.Clock()
delay = clock.tick()

keys_pressed = set()
done = False
last = 0
while not done:
    # delay until 1/60th of second
    while time.time() - last < 1/60: pass
    last = time.time()

    # pump events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            keys_pressed.add(event.key)
        if event.type == pygame.KEYUP:
            keys_pressed.remove(event.key)

    # update game state
    if pygame.K_ESCAPE in keys_pressed:
        done = True

    # update and draw

    surface.fill((0, 0, 0))
    if(ball.get_score_left()):
        delay = pygame.time.get_ticks()
        right_score = int(right_score) + 1
        right_score_text.update_text(WIDTH/4*3, 50,str(right_score))
    elif(ball.get_score_right()):
        delay = pygame.time.get_ticks()
        left_score = int(left_score) + 1
        left_score_text.update_text(WIDTH/4, 50,str(left_score))
    left_score_text.draw(surface)
    right_score_text.draw(surface)

    ball.draw(surface)
    if(pygame.time.get_ticks() - delay >= 1000):
        ball.update(paddles)

    for y in range(0, HEIGHT, int(HEIGHT/10)):
        rect = pygame.Rect(WIDTH/2, y, 1, int(HEIGHT/20))
        pygame.draw.rect(surface, pygame.Color(255, 255, 255, 255), rect)

    for paddle in paddles:
        paddle.update(keys_pressed, ball.get_x(), ball.get_y())
        paddle.draw(surface)
    

    pygame.display.update()

pygame.quit()
sys.exit()