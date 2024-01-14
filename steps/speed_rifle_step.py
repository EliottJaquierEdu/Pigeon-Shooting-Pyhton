import math
from abc import ABC

import pygame

from steps.angle_rifle_step import AngleRifleStep
from steps.step import Step


class SpeedRifleStep(Step, ABC):
    def __init__(self, rifle, pigeon):
        super().__init__(rifle, pigeon)
        self.initial_color = rifle.color
        self.initial_points_color = rifle.points_color

    def reset(self):
        super().reset()
        self.rifle.is_drawable = True
        self.rifle.is_points_drawn = True
        self.pigeon.is_drawable = True
        self.pigeon.is_points_drawn = False
        self.is_valid = False
        self.rifle.angle = 0

    def next_step(self):
        return AngleRifleStep(self.rifle, self.pigeon)

    def update(self, screen, mouse_position, time):
        if self.is_done:
            return
        super().update(screen, mouse_position, time)
        start_rifle_point = self.rifle.get_point(self.rifle.wait_time, screen.convert_vector_to_screen)

        mouse_relative_position = [mouse_position[0] - start_rifle_point[0], mouse_position[1] - start_rifle_point[1]]
        self.rifle.speed = mouse_relative_position[0] / screen.graph_size
        self.is_valid = 1000 >= self.rifle.speed >= 10
        self.rifle.color = self.rifle.default_color if self.is_valid else "Red"
        self.rifle.points_color = self.rifle.default_points_color if self.is_valid else "Red"

    def handle_event(self, event):
        super().handle_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and self.is_valid:
            self._is_done = True

    def step_description(self):
        return "Choissisez la vitesse (" + str(round(self.rifle.speed, 1)) + " m/s) du tir"
