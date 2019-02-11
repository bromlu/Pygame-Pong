#!/usr/bin/python3

import os
import sys
import time

import contextlib
with contextlib.redirect_stdout(None): import pygame

pygame.init()
pygame.display.set_caption('Pong')
screen = pygame.display.set_mode((600, 400))
surf = pygame.display.get_surface()

paddles = [
    pygame.Rect(40, 160, 10, 80),
    pygame.Rect(550, 160, 10, 80),
]
color = pygame.Color(255, 255, 255, 255)

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
    if pygame.K_UP in keys_pressed:
        paddles[0].y -= 10
    if pygame.K_DOWN in keys_pressed:
        paddles[0].y += 10
    if pygame.K_ESCAPE in keys_pressed:
        done = True

    # draw
    surf.fill((64, 64, 64))
    for paddle in paddles:
        pygame.draw.rect(surf, color, paddle)
    pygame.display.update()

pygame.quit()
sys.exit()