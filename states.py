import random
import math

from ball import Ball
from paddle import Paddle
from text import Text
from players import manual_player_1, manual_player_2, AI_player
from powers import Grow_Power, Shrink_Power

import contextlib
with contextlib.redirect_stdout(None): import pygame

MENU_MOVE = pygame.mixer.Sound("assets/sfx_menu_move1.wav")
MENU_SELECT = pygame.mixer.Sound("assets/sfx_menu_select1.wav")
WIN = pygame.mixer.Sound("assets/sfx_alarm_loop8.wav")

PADDLE_HEIGHT = 80
BALL_SIZE = 10
BALL_SPEED = 5
POWER_SIZE = 10
POWER_SPEED = 7

class Game:
    def __init__(self, width, height, player_1, player_2): 
        self.width = width
        self.height = height
        self.ball = Ball(width, height, BALL_SIZE, BALL_SPEED)
        self.paddles = [
            Paddle(550, 160, PADDLE_HEIGHT, width, height, player_1),
            Paddle(40, 160, PADDLE_HEIGHT, width, height, player_2)
        ]
        self.powers = []
        self.left_score = "0"
        self.right_score = "0"
        self.left_score_text = Text(width/4, 50, self.left_score)
        self.right_score_text = Text(width/4*3, 50, self.right_score)

        self.clock = pygame.time.Clock()
        self.time_of_score = pygame.time.get_ticks()

    def update(self, keys_pressed, surface):
        randomInt = random.randint(0, 200)
        if randomInt == 7:
            self.spawn_power(surface, Grow_Power)
        elif randomInt == 42 or randomInt == 69:
            self.spawn_power(surface, Shrink_Power)
        

        self.ball.draw(surface)
        if(self.ball.get_score_left()):
            self.time_of_score = pygame.time.get_ticks()
            self.right_score = int(self.right_score) + 1
            self.right_score_text.update_text(self.width/4*3, 50,str(self.right_score))
        elif(self.ball.get_score_right()):
            self.time_of_score = pygame.time.get_ticks()
            self.left_score = int(self.left_score) + 1
            self.left_score_text.update_text(self.width/4, 50,str(self.left_score))
        self.left_score_text.draw(surface)
        self.right_score_text.draw(surface)

        if(pygame.time.get_ticks() - self.time_of_score >= 1000):
            self.ball.update(self.paddles)

        for y in range(0, self.height, int(self.height/10)):
            rect = pygame.Rect(self.width/2, y, 1, int(self.height/20))
            pygame.draw.rect(surface, pygame.Color(255, 255, 255, 255), rect)

        for paddle in self.paddles:
            paddle.update(keys_pressed, self.ball.get_x(), self.ball.get_y())
            paddle.draw(surface)

        for power in self.powers:
            if not power.get_collected():
                power.update(self.paddles)
                power.draw(surface)
            elif power.get_delete():
                self.powers.remove(power)

        if int(self.left_score) >= 10:
            pygame.mixer.stop()
            WIN.play(2)
            return Flash(self.width, self.height, self.right_score_text, self.left_score_text, self.paddles, "Player 2 wins!")
        elif int(self.right_score) >= 10:
            pygame.mixer.stop()
            WIN.play(2)
            return Flash(self.width, self.height, self.left_score_text, self.right_score_text, self.paddles, "Player 1 wins!")
        return self

    def spawn_power(self, surface, power_type):
        vx = 0
        while(vx < 2 and vx > -2):
            angle = random.uniform(0, 2 * math.pi)
            vx = math.cos(angle) * POWER_SPEED
            vy = math.sin(angle) * POWER_SPEED
        x = self.width/2 - POWER_SIZE/2
        y = random.randint(0,self.height - POWER_SIZE)
        self.powers.append(power_type(x, y, POWER_SIZE, self.width, self.height, vx, vy))


class Menu:
    def __init__(self, width, height): 
        self.width = width
        self.height = height

        self.options = [
            { 
                "text": "2 Player", 
                "text_index": 3, 
                "x": self.width/2, 
                "y": self.height/2 - 32,
                "state": Game(self.width, self.height, manual_player_1, manual_player_2) 
            },
            { 
                "text": "1 Player", 
                "text_index": 4, 
                "x": self.width/2, 
                "y": self.height/2,
                "state": Game(self.width, self.height, manual_player_1, AI_player)
            },
            { 
                "text": "0 Player", 
                "text_index": 5, 
                "x": self.width/2, 
                "y": self.height/2 + 32, 
                "state": Game(self.width, self.height, AI_player, AI_player) 
            },
            { 
                "text": "Instructions", 
                "text_index": 6, 
                "x": self.width/2, 
                "y": self.height/4 * 3, 
                "state": Instruction(self.width, self.height) 
            },
            { 
                "text": "Thanks", 
                "text_index": 7, 
                "x": self.width/2, 
                "y": self.height/4 * 3 + 34, 
                "state": Thanks(self.width, self.height) 
            },
        ]

        self.text = [
            Text(self.width/2, self.height/5, "Pong", 72),
            Text(self.width/2, self.height/5 + 30, "By Luke Brom", 12),
            Text(self.width/2, self.height - 14, "(Hit escape to exit at any time)", 12)
        ]
        for option in self.options:
            self.text.append(Text(option["x"], option["y"], option["text"], 32))

        self.selected = 0
        self.clock = pygame.time.Clock()
        self.time_since_button_pressed = self.clock.tick()

    def update(self, keys_pressed, surface):
        self.update_selected(keys_pressed)

        if pygame.K_RETURN in keys_pressed or pygame.K_KP_ENTER in keys_pressed:
            MENU_SELECT.play()
            return self.options[self.selected]["state"]

        for text in self.text:
            text.draw(surface)

        return self

    def update_selected(self, keys_pressed):
        option = self.options[self.selected]
        self.text[option["text_index"]].update_text(option["x"], option["y"], option["text"], (34,139,34))

        if(pygame.time.get_ticks() - self.time_since_button_pressed >= 100):
            if pygame.K_UP in keys_pressed:
                MENU_MOVE.play()
                self.text[option["text_index"]].update_text(option["x"], option["y"], option["text"])
                if self.selected == 0:
                    self.selected = len(self.options) - 1
                else:
                    self.selected -= 1
                self.time_since_button_pressed = pygame.time.get_ticks()

            if pygame.K_DOWN in keys_pressed:
                MENU_MOVE.play()
                self.text[option["text_index"]].update_text(option["x"], option["y"], option["text"])
                if self.selected == len(self.options) - 1:
                    self.selected = 0
                else:
                    self.selected += 1
                self.time_since_button_pressed = pygame.time.get_ticks()

class Endgame:
    def __init__(self, width, height, message): 
        self.width = width
        self.height = height

        self.text = [
            Text(self.width/2, self.height/5, "Game Over", 72),
            Text(self.width/2, self.height/5 + 50, "(Hit backspace or delete to return to menu)", 12),
            Text(self.width/2, self.height/2, message, 32),
            Text(self.width/2, self.height - 14, "(Hit escape to exit at any time)", 12)
        ]

    def update(self, keys_pressed, surface):
        if pygame.K_DELETE in keys_pressed or pygame.K_BACKSPACE in keys_pressed:
            MENU_SELECT.play()
            return Menu(self.width, self.height)

        for text in self.text:
            text.draw(surface)

        return self

class Instruction:
    def __init__(self, width, height): 
        self.width = width
        self.height = height

        self.text = [
            Text(self.width/2, self.height/5, "Instructions", 72),
            Text(self.width/2, self.height/5 + 50, "(Hit backspace or delete to return to menu)", 12),
            Text(self.width/2, self.height/2 - 26, "Player One: Up and Down arrows to move paddle, ? for powerup.", 16),
            Text(self.width/2, self.height/2 - 10, "Player Two: W (up) and S (down) to move paddle, e for powerup", 16),
            Text(self.width/2, self.height/2 + 10, "Green Powerups grow your paddle", 16),
            Text(self.width/2, self.height/2 + 26, "Red Powerups fire shrink rays at your opponent", 16),
            Text(self.width/2, self.height - 14, "(Hit escape to exit at any time)", 12)
        ]

    def update(self, keys_pressed, surface):
        if pygame.K_DELETE in keys_pressed or pygame.K_BACKSPACE in keys_pressed:
            MENU_SELECT.play()
            return Menu(self.width, self.height)

        for text in self.text:
            text.draw(surface)

        return self

class Flash:
    def __init__(self, width, height, loser_score, winner_score, paddles, message):
        self.height = height
        self.width = width
        self.loser_score = loser_score
        self.winner_score = winner_score
        self.paddles = paddles
        self.message = message

        self.time_started = pygame.time.get_ticks()
        self.time_since_last_flash = 0
        self.draw = True

    def update(self, keys_pressed, surface):
        if(self.draw):
            self.winner_score.draw(surface)

        self.time_since_last_flash += 1
        if (self.time_since_last_flash >= 6):
            self.draw = not self.draw
            self.time_since_last_flash = 0

        self.loser_score.draw(surface)

        for y in range(0, self.height, int(self.height/10)):
            rect = pygame.Rect(self.width/2, y, 1, int(self.height/20))
            pygame.draw.rect(surface, pygame.Color(255, 255, 255, 255), rect)

        for paddle in self.paddles:
            paddle.draw(surface)

        if(pygame.time.get_ticks() - self.time_started >= 2000):
            return Endgame(self.width, self.height, self.message)

        return self

class Thanks:
    def __init__(self, width, height): 
        self.width = width
        self.height = height

        self.text = [
            Text(self.width/2, self.height/5, "Special Thanks", 72),
            Text(self.width/2, self.height/5 + 50, "(Hit backspace or delete to return to menu)", 12),
            Text(self.width/2, self.height/2 - 26, "To dl-sounds and Subspace Audio for their", 16),
            Text(self.width/2, self.height/2 - 10, "awesome public domain music and effects!", 16),
            Text(self.width/2, self.height/2 + 10, "Also thanks to Dr. Denning and Edric Lamar", 16),
            Text(self.width/2, self.height/2 + 26, "For all of the things they taught me", 16),
            Text(self.width/2, self.height - 14, "(Hit escape to exit at any time)", 12)
        ]

    def update(self, keys_pressed, surface):
        if pygame.K_DELETE in keys_pressed or pygame.K_BACKSPACE in keys_pressed:
            MENU_SELECT.play()
            return Menu(self.width, self.height)

        for text in self.text:
            text.draw(surface)

        return self