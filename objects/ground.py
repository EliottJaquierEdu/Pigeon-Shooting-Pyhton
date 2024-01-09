import pygame

from objects.drawable_objet import DrawableObject


class Ground(DrawableObject):
    def __init__(self, ground_color):
        super().__init__()
        self.ground_color = ground_color

    def draw(self, screen, width, height, space_conversion_fn):
        if not self.is_drawable:
            return
        zeros = space_conversion_fn([0, 0])
        rect = pygame.Rect(0, zeros[1], width, height - zeros[1])
        pygame.draw.rect(screen, self.ground_color, rect)