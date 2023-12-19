import math
from abc import ABC

from graph_line import GraphLine


class Pigeon(GraphLine, ABC):
    def __init__(self, color, min_time, max_time, samples):
        super().__init__(color, min_time, max_time, samples)
        self.start_x = 0
        self.start_y = 1
        self.speed = 20
        self.angle = 60
        self.mass = 0.1

    def x(self, t):
        return self.start_x + math.cos(math.radians(self.angle)) * self.speed * t

    def y(self, t):
        return self.start_y + math.sin(math.radians(self.angle)) * self.speed * t - (9.81 / 2) * math.pow(t, 2)
