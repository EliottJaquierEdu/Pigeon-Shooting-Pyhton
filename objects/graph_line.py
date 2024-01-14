from abc import ABC, abstractmethod

import pygame

import utils
from objects.drawable_objet import DrawableObject


class GraphLine(ABC, DrawableObject):
    def __init__(self, color, line_width, min_time, max_time, samples, points_color, points_radius):
        super().__init__()
        self._min_time = min_time
        self._max_time = max_time
        self._samples = samples
        self.color = color
        self.default_color = color
        self.line_width = line_width
        self.points_color = points_color
        self.default_points_color = points_color
        self.points_radius = points_radius
        self.is_points_drawn = False

        self._need_refresh = True

    @property
    def min_time(self):
        return self._min_time

    @min_time.setter
    def min_time(self, new_min_time):
        self._min_time = new_min_time
        self._need_refresh = True

    @property
    def max_time(self):
        return self._max_time

    @max_time.setter
    def max_time(self, new_max_time):
        self._max_time = new_max_time
        self._need_refresh = True

    @property
    def samples(self):
        return self._samples

    @samples.setter
    def samples(self, new_samples):
        self._samples = new_samples
        self._need_refresh = True

    @abstractmethod
    def x(self, t):
        pass

    @abstractmethod
    def y(self, t):
        pass

    def get_point(self, t, space_conversion_fn):
        return space_conversion_fn([self.x(t), self.y(t)])

    def get_lines(self, space_conversion_fn):
        points = []
        for i in range(self._samples + 1):
            percentage = i / self._samples
            time = utils.lerp(self._min_time, self._max_time, percentage)
            point = self.get_point(time, space_conversion_fn)
            points.append(point)
        return points

    def draw(self, screen, width, height, space_conversion_fn):
        if not self.is_drawable:
            return
        lines = self.get_lines(space_conversion_fn)
        pygame.draw.lines(screen, self.color, False, lines, self.line_width)
        if self.is_points_drawn:
            for i in range(round(((self._max_time + 0.09) - self._min_time) * 10)):
                pygame.draw.circle(screen, self.points_color, self.get_point(self._min_time + i / 10, space_conversion_fn),
                               self.points_radius if (i % 10 == 0) else self.points_radius / 1.75)