import math
from abc import ABC

import pygame

from steps.simlulate_time_with_mouse_step import SimulateTimeWithMouseStep
from steps.step import Step


class AngleRifleStep(Step, ABC):
    def __init__(self):
        super().__init__()
        self.is_valid = False

    def next_step(self):
        return SimulateTimeWithMouseStep()

    def update(self, screen, mouse_position, time, rifle, pigeon):
        if self.is_done:
            return
        start_rifle_point = rifle.get_point(rifle.shoot_t, screen.convert_vector_to_screen)

        mouse_relative_position = [mouse_position[0] - start_rifle_point[0], mouse_position[1] - start_rifle_point[1]]
        angle = -math.atan2(mouse_relative_position[1], mouse_relative_position[0])
        rifle.angle = math.degrees(angle)
        self.is_valid = rifle.angle >= 0
        rifle.color = "Black" if self.is_valid else "Red"

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and self.is_valid:
            self._is_done = True


    def step_description(self):
        return "Choissisez l'angle du tir"
