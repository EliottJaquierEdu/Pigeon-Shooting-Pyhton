import math
from abc import ABC

import pygame

from steps.place_rifle_step import PlaceRifleStep
from steps.step import Step


class AnglePigeonStep(Step, ABC):
    def __init__(self, rifle, pigeon):
        super().__init__(rifle, pigeon)
        rifle.is_drawable = False
        pigeon.is_drawable = True
        self.is_valid = False

    def next_step(self):
        return PlaceRifleStep(self.rifle, self.pigeon)

    def update(self, screen, mouse_position, time):
        if self.is_done:
            return
        start_pigeon_point = self.pigeon.get_point(0, screen.convert_vector_to_screen)

        mouse_relative_position = [mouse_position[0] - start_pigeon_point[0], mouse_position[1] - start_pigeon_point[1]]
        angle = -math.atan2(mouse_relative_position[1], mouse_relative_position[0])
        self.pigeon.angle = math.degrees(angle)
        if self.pigeon.angle > 89:
            self.pigeon.angle = 89
        if self.pigeon.angle < 0:
            self.pigeon.angle = 0

        self.pigeon.draw_point_in_time(screen.screen, screen.convert_vector_to_screen, "white", 7)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            self._is_done = True

    def step_description(self):
        return "Choissisez l'angle (" + str(round(self.pigeon.angle, 1)) + "°) du pigeon"
