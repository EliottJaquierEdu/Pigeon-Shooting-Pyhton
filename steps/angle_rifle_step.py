import math
from abc import ABC

import pygame

from steps.simlulate_time_with_mouse_step import SimulateTimeWithMouseStep
from steps.step import Step


class AngleRifleStep(Step, ABC):
    def __init__(self, rifle, pigeon):
        super().__init__(rifle, pigeon)
        rifle.is_drawable = True
        rifle.is_points_drawn = True
        pigeon.is_drawable = True
        pigeon.is_points_drawn = False
        self.is_valid = False
        self.initial_color = rifle.color
        self.initial_points_color = rifle.points_color

    def next_step(self):
        return SimulateTimeWithMouseStep(self.rifle, self.pigeon)

    def update(self, screen, mouse_position, time):
        if self.is_done:
            return
        start_rifle_point = self.rifle.get_point(self.rifle.wait_time, screen.convert_vector_to_screen)

        mouse_relative_position = [mouse_position[0] - start_rifle_point[0], mouse_position[1] - start_rifle_point[1]]
        angle = -math.atan2(mouse_relative_position[1], mouse_relative_position[0])
        self.rifle.angle = math.degrees(angle)
        self.is_valid = self.rifle.angle >= 0 and not(86 < self.rifle.angle < 90.1)
        self.rifle.color = self.initial_color if self.is_valid else "Red"
        self.rifle.points_color = self.initial_points_color if self.is_valid else "Red"

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and self.is_valid:
            self._is_done = True

    def step_description(self):
        return "Choissisez l'angle (" + str(round(self.rifle.angle, 1)) + "°) du tir"
