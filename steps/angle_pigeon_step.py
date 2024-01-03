import math
from abc import ABC

import pygame

from steps.speed_pigeon_step import SpeedPigeonStep
from steps.step import Step


class AnglePigeonStep(Step, ABC):
    def next_step(self):
        return SpeedPigeonStep()

    def update(self, screen, mouse_position, rifle, pigeon):
        if self.is_done:
            return
        start_pigeon_point = pigeon.get_point(0, screen.convert_vector_to_screen)

        mouse_relative_position = [mouse_position[0] - start_pigeon_point[0], mouse_position[1] - start_pigeon_point[1]]
        angle = -math.atan2(mouse_relative_position[1], mouse_relative_position[0])
        pigeon.angle = math.degrees(angle)
        if pigeon.angle > 89:
            pigeon.angle = 89
        if pigeon.angle < 0:
            pigeon.angle = 0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            self._is_done = True


    def step_description(self):
        return "Choissisez l'angle du pigeon"
