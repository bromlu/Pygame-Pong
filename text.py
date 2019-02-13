import contextlib
with contextlib.redirect_stdout(None): import pygame
import pygame.freetype

pygame.freetype.init()

class Text:
    def __init__(self, x, y, text, size=48, color=(255,255,255)):
        self.font = pygame.freetype.Font("assets/ConnectionII.otf", size)

        self.update_text(x, y, text, color)

    def draw(self, surface):
        surface.blit(self.surface, pygame.Rect(self.x, self.y, self.width, self.height))

    def update_text(self, x, y, text, color=(255,255,255)):
        self.surface, rect = self.font.render(text, color, (0,0,0))
        self.width = rect.width
        self.height = rect.height
        self.x = x - self.width/2
        self.y = y - self.height/2