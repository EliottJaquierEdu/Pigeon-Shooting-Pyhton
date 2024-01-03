import pygame
from pygame import Rect


class HUD:
    def __init__(self, title, title_color, text_color, background_color):
        self.title = title
        self.title_color = title_color
        self.text_color = text_color
        self.title_font = pygame.font.SysFont('Open Sans', 36)
        self.text_font = pygame.font.SysFont('Open Sans', 24)
        self.background_color = background_color

    def draw(self, surface, width, height):
        pygame.draw.rect(surface, self.background_color, Rect(0, 0, width, 48 + 24))
        center = width / 2
        self.draw_text(surface, self.title_font, self.title, self.title_color, center, 12)
        self.draw_text(surface, self.text_font, "Aucune étape", self.text_color, center, 48)

    def draw_text(self, surface, font, title, color, x, y, alignment=0.5):
        text_size = font.size(title)
        surface.blit(font.render(str(title), True, color), [x - text_size[0] * alignment, y])
