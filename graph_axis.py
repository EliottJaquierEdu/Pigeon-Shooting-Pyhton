import pygame.draw


class GraphAxis:
    def __init__(self, name, unit, scale, color):
        self.name = name
        self.unit = unit
        self.scale = scale
        self.color = color

    def draw(self, surface):
        pygame.draw.line(surface,self.color)