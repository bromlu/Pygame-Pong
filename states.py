from ball import Ball
from paddle import Paddle
from text import Text

from players import manual_player_1, manual_player_2, AI_player

import contextlib
with contextlib.redirect_stdout(None): import pygame

PADDLE_HEIGHT = 80
BALL_SIZE = 10
BALL_SPEED = 5

class Game:
    def __init__(self, width, height, player_1, player_2): 
        self.width = width
        self.height = height
        self.ball = Ball(width, height, BALL_SIZE, BALL_SPEED)
        self.paddles = [
            Paddle(550, 160, PADDLE_HEIGHT, width, height, player_1),
            Paddle(40, 160, PADDLE_HEIGHT, width, height, player_2)
        ]
        self.left_score = "0"
        self.right_score = "0"
        self.left_score_text = Text(width/4, 50, self.left_score)
        self.right_score_text = Text(width/4*3, 50, self.right_score)

        self.clock = pygame.time.Clock()
        self.time_of_score = self.clock.tick()

    def update(self, keys_pressed, surface):
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

        self.ball.draw(surface)
        if(pygame.time.get_ticks() - self.time_of_score >= 1000):
            self.ball.update(self.paddles)

        for y in range(0, self.height, int(self.height/10)):
            rect = pygame.Rect(self.width/2, y, 1, int(self.height/20))
            pygame.draw.rect(surface, pygame.Color(255, 255, 255, 255), rect)

        for paddle in self.paddles:
            paddle.update(keys_pressed, self.ball.get_x(), self.ball.get_y())
            paddle.draw(surface)

        return self

class Menu:
    def __init__(self, width, height): 
        self.width = width
        self.height = height

        self.options = [
            { 
                "text": "2 Player", 
                "text_index": 2, 
                "x": self.width/2, 
                "y": self.height/2 - 32,
                "state": Game(self.width, self.height, manual_player_1, manual_player_2) 
            },
            { 
                "text": "1 Player", 
                "text_index": 3, 
                "x": self.width/2, 
                "y": self.height/2,
                "state": Game(self.width, self.height, manual_player_1, AI_player)
            },
            { 
                "text": "0 Player", 
                "text_index": 4, 
                "x": self.width/2, 
                "y": self.height/2 + 32, 
                "state": Game(self.width, self.height, AI_player, AI_player) 
            },
            { 
                "text": "Instructions", 
                "text_index": 5, 
                "x": self.width/2, 
                "y": self.height/5 * 4, 
                "state": Instruction(self.width, self.height) 
            },
        ]

        self.text = [
            Text(self.width/2, self.height/5, "Pong", 72),
            Text(self.width/2, self.height/5 + 30, "By Luke Brom", 12)
        ]
        for option in self.options:
            self.text.append(Text(option["x"], option["y"], option["text"], 32))

        self.selected = 0
        self.clock = pygame.time.Clock()
        self.time_since_button_pressed = self.clock.tick()

    def update(self, keys_pressed, surface):
        self.update_selected(keys_pressed)

        if pygame.K_RETURN in keys_pressed or pygame.K_KP_ENTER in keys_pressed:
            return self.options[self.selected]["state"]

        for text in self.text:
            text.draw(surface)

        return self

    def update_selected(self, keys_pressed):
        option = self.options[self.selected]
        self.text[option["text_index"]].update_text(option["x"], option["y"], option["text"], (34,139,34))

        if(pygame.time.get_ticks() - self.time_since_button_pressed >= 100):
            if pygame.K_UP in keys_pressed:
                self.text[option["text_index"]].update_text(option["x"], option["y"], option["text"])
                if self.selected == 0:
                    self.selected = len(self.options) - 1
                else:
                    self.selected -= 1
                self.time_since_button_pressed = pygame.time.get_ticks()

            if pygame.K_DOWN in keys_pressed:
                self.text[option["text_index"]].update_text(option["x"], option["y"], option["text"])
                if self.selected == len(self.options) - 1:
                    self.selected = 0
                else:
                    self.selected += 1
                self.time_since_button_pressed = pygame.time.get_ticks()

class Endgame:
    def __init__(self, width, height): 
        self.width = width
        self.height = height

        self.left_score_text = Text(width/4, 50, "self.left_score", 16)
        self.right_score_text = Text(width/4*3, 50, "self.right_score", 16)

    def update(self, keys_pressed, surface):
        return self

class Instruction:
    def __init__(self, width, height): 
        self.width = width
        self.height = height

        self.text = [
            Text(self.width/2, self.height/5, "Instructions", 72),
            Text(self.width/2, self.height/2 - 10, "Player One: Up and Down arrows to move paddle", 16),
            Text(self.width/2, self.height/2 + 10, "Player Two: W (up) and S (down) to move paddle", 16)
        ]

    def update(self, keys_pressed, surface):
        if pygame.K_DELETE in keys_pressed or pygame.K_BACKSPACE in keys_pressed:
            return Menu(self.width, self.height)

        for text in self.text:
            text.draw(surface)

        return self