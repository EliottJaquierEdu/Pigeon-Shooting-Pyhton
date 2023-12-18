import math


class Pigeon:
    start_x = 0
    start_y = 1
    speed = 20
    angle = 60

    def x(self, t):
        return self.start_x + math.cos(math.radians(self.angle)) * self.speed * t

    def y(self, t):
        return self.start_y + math.sin(math.radians(self.angle)) * self.speed * t - (9.81 / 2) * math.pow(t, 2)
