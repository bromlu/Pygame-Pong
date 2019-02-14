#!/usr/bin/python3

import os
import sys
import time

from players import manual_player_1, manual_player_2, AI_player

import contextlib
with contextlib.redirect_stdout(None): import pygame

WIDTH = 600
HEIGHT = 400

pygame.mixer.init()
pygame.font.init()
pygame.display.set_caption('Pong')
from states import Menu

#https://www.dl-sounds.com/royalty-free/off-limits/
pygame.mixer.music.load('assets/Off_Limits.wav')
pygame.mixer.music.play(loops=-1)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
surface= pygame.display.get_surface()

state = Menu(WIDTH, HEIGHT)

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
    state = state.update(keys_pressed, surface)
    pygame.display.update()

pygame.mixer.music.stop()
pygame.quit()
sys.exit()