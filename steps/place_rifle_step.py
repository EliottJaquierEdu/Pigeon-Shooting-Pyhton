from abc import ABC

import pygame

from steps.angle_rifle_step import AngleRifleStep
from steps.step import Step


class PlaceRifleStep(Step, ABC):
    def __init__(self, rifle, pigeon):
        super().__init__(rifle, pigeon)
        rifle.is_drawable = True
        pigeon.is_drawable = True
        self.is_valid = False
        self.initial_color = rifle.color

    def next_step(self):
        return AngleRifleStep(self.rifle, self.pigeon)

    def update(self, screen, mouse_position, time):
        if self.is_done:
            return
        mouse_position_vector_space = screen.convert_screen_to_vector(mouse_position)
        self.rifle.start_x = mouse_position_vector_space[0]
        self.rifle.start_y = mouse_position_vector_space[1]

        max_height = self.pigeon.y(self.pigeon.t(self.rifle.start_x))
        self.is_valid = max_height > self.rifle.start_y > 0 and self.rifle.start_x > 0

        self.rifle.color = self.initial_color if self.is_valid else "Red"
        self.rifle.draw_point_in_time(screen.screen, screen.convert_vector_to_screen, "white" if self.is_valid else "Red", 7)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and self.is_valid:
            self._is_done = True

    def step_description(self):
        return "Placez le fusil en dessous du pigeon (x : " + str(round(self.rifle.start_x, 1)) + " m  y : " + str(
            round(self.rifle.start_y, 1)) + " m)"
