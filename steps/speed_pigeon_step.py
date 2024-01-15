import math
from abc import ABC

import pygame

from steps.angle_pigeon_step import AnglePigeonStep
from steps.step import Step


class SpeedPigeonStep(Step, ABC):
    def reset(self):
        super().reset()
        self.is_valid = False
        self.rifle.is_drawable = False
        self.rifle.is_points_drawn = False
        self.pigeon.is_drawable = True
        self.pigeon.is_points_drawn = True
        self.pigeon.angle = 60

    def next_step(self):
        return AnglePigeonStep(self.rifle, self.pigeon)

    def update(self, screen, mouse_position, time):
        if self.is_done:
            return
        super().update(screen, mouse_position, time)
        mouse_position_vector_space = screen.convert_screen_to_vector(mouse_position)
        if (mouse_position_vector_space[0] < 0):
            mouse_position_vector_space[0] = 0
        self.pigeon.speed = math.sqrt(mouse_position_vector_space[0]) * 3.5
        if (self.pigeon.speed < 2):
            self.pigeon.speed = 2

        self.is_valid = 100 > self.pigeon.speed

        self.pigeon.color = self.pigeon.default_color if self.is_valid else "Red"
        self.pigeon.points_color = self.pigeon.default_points_color if self.is_valid else "Red"

    def handle_event(self, event):
        super().handle_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and self.is_valid:
            self._is_done = True

    def step_description(self):
        return "Changez la vitesse du pigeon avec votre souris et valider la vitesse (" + str(
            round(self.pigeon.speed, 1)) + " m/s) avec un click droit"
