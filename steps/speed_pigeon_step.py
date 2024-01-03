import math
from abc import ABC

import pygame

from steps.angle_pigeon_step import AnglePigeonStep
from steps.step import Step


class SpeedPigeonStep(Step, ABC):
    def __init__(self):
        super().__init__()
        self.is_valid = False

    def next_step(self):
        return AnglePigeonStep()

    def update(self, screen, mouse_position, time, rifle, pigeon):
        if self.is_done:
            return
        mouse_position_vector_space = screen.convert_screen_to_vector(mouse_position)
        if(mouse_position_vector_space[0] < 0):
            mouse_position_vector_space[0] = 0
        pigeon.speed = math.sqrt(mouse_position_vector_space[0])*3.5
        if(pigeon.speed < 2):
            pigeon.speed = 2

        self.is_valid = 100 > pigeon.speed

        pigeon.color = "Black" if self.is_valid else "Red"

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and self.is_valid:
            self._is_done = True

    def step_description(self):
        return "Changez la vitesse du pigeon avec votre souris et valider la vitesse avec un click droit"
