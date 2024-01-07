from abc import ABC

import pygame

from steps.speed_pigeon_step import SpeedPigeonStep
from steps.step import Step


class BootStep(Step, ABC):
    def __init__(self, rifle, pigeon):
        super().__init__(rifle, pigeon)
        self.lines = [
            "Bienvenue sur ce programme de tir au pigeon d'argile! Passez à l'étape suivante avec un click droit.",
            "Déplacez-vous en maintenant le click gauche et zoomez avec la molette. (Continuez avec un click droit)"
        ]
        self.current_line = 0

    def next_step(self):
        return SpeedPigeonStep(self.rifle, self.pigeon)

    def update(self, screen, mouse_position, time):
        if self.is_done:
            return

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            if (self.current_line < len(self.lines) - 1):
                self.current_line += 1
            else:
                self._is_done = True

    def step_description(self):
        return self.lines[self.current_line]
