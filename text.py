import contextlib
with contextlib.redirect_stdout(None): import pygame
import pygame.freetype

pygame.freetype.init()

class Text:
    def __init__(self, x, y, text):
        self.font = pygame.freetype.Font("assets/ConnectionII.otf", 48)

        self.update_text(x, y, text)

    def draw(self, surface):
        surface.blit(self.surface, pygame.Rect(self.x, self.y, self.width, self.height))

    def update_text(self, x, y, text):
        self.surface, rect = self.font.render(text, (255,255,255), (0,0,0))
        self.width = rect.width
        self.height = rect.height
        self.x = x - self.width/2
        self.y = y - self.height/2