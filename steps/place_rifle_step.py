from abc import ABC

import pygame

from steps.angle_rifle_step import AngleRifleStep
from steps.step import Step


class PlaceRifleStep(Step, ABC):
    def __init__(self):
        super().__init__()
        self.is_valid = False

    def next_step(self):
        return AngleRifleStep()

    def update(self, screen, mouse_position, rifle, pigeon):
        if self.is_done:
            return
        mouse_position_vector_space = screen.convert_screen_to_vector(mouse_position)
        rifle.start_x = mouse_position_vector_space[0]
        rifle.start_y = mouse_position_vector_space[1]

        max_height = pigeon.y(pigeon.t(rifle.start_x))
        self.is_valid = max_height > rifle.start_y > 0 and rifle.start_x > 0

        rifle.color = "Black" if self.is_valid else "Red"

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and self.is_valid:
            self._is_done = True

    def step_description(self):
        return "Placez le fusil (il doit être en dessous du pigeon)"
