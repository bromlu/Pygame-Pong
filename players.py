import contextlib
with contextlib.redirect_stdout(None): import pygame

def manual_player_1(paddle, keys_pressed, ball_x, ball_y):
    if pygame.K_UP in keys_pressed:
        paddle.rect.y -= 10
    if pygame.K_DOWN in keys_pressed:
        paddle.rect.y += 10

def manual_player_2(paddle, keys_pressed, ball_x, ball_y):
    if pygame.K_w in keys_pressed:
        paddle.rect.y -= 10
    if pygame.K_s in keys_pressed:
        paddle.rect.y += 10

def AI_player(paddle, keys_pressed, ball_x, ball_y):
    if abs(ball_x - paddle.rect.x) < 100:
        if ball_y > paddle.rect.y:
            paddle.rect.y += 5
        elif ball_y < paddle.rect.y + paddle.height:
            paddle.rect.y -= 5