import pygame
from pygame import Rect


class HUD:
    def __init__(self, title, title_color, text_color, background_color, initial_step):
        self.title = title
        self.title_color = title_color
        self.text_color = text_color
        self.title_font = pygame.font.SysFont('Open Sans', 36)
        self.text_font = pygame.font.SysFont('Open Sans', 24)
        self.back_button = pygame.font.SysFont('Open Sans', 72)
        self.background_color = background_color
        self.step = initial_step

    def draw(self, surface, width, height):
        pygame.draw.rect(surface, self.background_color, Rect(0, 0, width, 48 + 24))
        center = width / 2
        self.draw_text(surface, self.title_font, self.title, self.title_color, center, 12)
        self.step.on_hud(surface, width, height, self.draw_text, self.text_font, self.text_color)
        if self.step.previous_step is not None:
            pygame.draw.rect(surface, self.title_color, Rect(6, 6, 48 + 12, 48 + 12))
            self.draw_text(surface, self.back_button, "<", self.background_color, 20, 8, 0)

    def draw_text(self, surface, font, title, color, x, y, alignment=0.5):
        text_size = font.size(title)
        surface.blit(font.render(str(title), True, color), [x - text_size[0] * alignment, y])

    def set_step(self, step):
        self.step = step
