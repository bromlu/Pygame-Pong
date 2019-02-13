import contextlib
with contextlib.redirect_stdout(None): import pygame

class Text:
    def __init__(self, x, y, text):
        self.font = pygame.font.Font(None, 48)
        self.surface= self.font.render(text, 1, (255,255,255), (0,0,0))
        
        rect = self.surface.get_rect()
        self.width = rect.width
        self.height = rect.height
        self.x = x - self.width/2
        self.y = y - self.height/2

    def draw(self, surface):
        surface.blit(self.surface, pygame.Rect(self.x, self.y, self.width, self.height))

    def update_text(self, text):
        self.surface= self.font.render(text, 1, (255,255,255), (0,0,0))