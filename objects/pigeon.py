import math
import random
from abc import ABC

import pygame.image

from objects.graph_line import GraphLine


class Pigeon(GraphLine, ABC):
    def __init__(self, color, line_width, min_time, max_time, samples):
        super().__init__(color, line_width, min_time, max_time, samples)
        self.start_x = 0
        self.start_y = 1
        self.speed = 20
        self.angle = 60
        self.acceleration = -9.81

        self.image = pygame.image.load("res/pigeonArgile.png")
        self.image_fragments = []
        for i in range(4):
            self.image_fragments.append(pygame.image.load("res/pigeonArgileF" + str(i + 1) + ".png"))

    def x(self, t):
        return self.start_x + math.cos(math.radians(self.angle)) * self.speed * t

    def y(self, t):
        return self.start_y + math.sin(math.radians(self.angle)) * self.speed * t + (self.acceleration / 2) * math.pow(
            t, 2)

    def get_point(self, t, space_conversion_fn, x_offset=0, y_offset=0):
        if t < 0:
            t = 0

        x = self.x(t) + x_offset
        y = self.y(t) + y_offset

        # Special case when the pigeon land
        if (y < 0):
            zeros = self.time_when_zeros(y_offset)
            time_when_landed = max(zeros[0], zeros[1])
            new_x = self.x(time_when_landed) + x_offset
            removed_from_x = (x - new_x)
            if removed_from_x > 0:
                x = math.log2(removed_from_x + 1) + new_x
            y = 0
        return space_conversion_fn([x, y])

    def t(self, x):
        return (x - self.start_x) / (math.cos(math.radians(self.angle)) * self.speed)

    def time_when_zeros(self, y_offset=0):
        c = self.start_y + y_offset
        b = math.sin(math.radians(self.angle)) * self.speed
        a = - (9.81 / 2)
        delta = math.pow(b, 2) - 4 * a * c
        if (delta < 0):
            # There are no zeros for this function on pigeon so use the max height
            top = (-b) / (2 * a)
            return [top, top]
        t1 = (-b + math.sqrt(delta)) / (2 * a)
        t2 = (-b - math.sqrt(delta)) / (2 * a)
        return [t1, t2]

    def draw_image_representation(self, display, t, t_when_impact, space_conversion_fn):
        images_to_draw = []
        random.seed(1)
        if (t > t_when_impact):
            # Draw fragments with a little offset (not physically based)
            for fragment in self.image_fragments:
                debris_speed = 10
                x_rand = (random.random() - 0.5)
                y_rand = (random.random() - 0.5)
                # Approximation of landing time
                zeros = self.time_when_zeros()
                t_landing = max(zeros[0], zeros[1])
                max_t_after_impact = min(t, t_landing) - t_when_impact
                images_to_draw.append(
                    [fragment, x_rand * max_t_after_impact * debris_speed, y_rand * max_t_after_impact * debris_speed])
        else:
            images_to_draw.append([self.image, 0, 0])

        for image in images_to_draw:
            points = self.get_point(t, space_conversion_fn, image[1], image[2])
            points[0] = points[0] - (image[0].get_width() / 2)
            points[1] = points[1] - (image[0].get_height() / 2)
            display.blit(image[0], points)
