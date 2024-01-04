import math
from abc import ABC

import pygame

from steps.step import Step


class SimulateTimeWithMouseStep(Step, ABC):
    def __init__(self):
        super().__init__()

    def next_step(self):
        return None

    def update(self, screen, mouse_position, playtime, rifle, pigeon):
        if self.is_done:
            return
        mouse_position_vector_space = screen.convert_screen_to_vector(mouse_position)
        time = pigeon.t(mouse_position_vector_space[0])
        rifle.play_audio(time, playtime)
        intersecting_time = rifle.time_intersecting_with_pigeon(pigeon)
        rifle.wait_time = rifle.waiting_time_to_intersect(pigeon)
        pigeon.draw_image_representation(screen.screen, time, intersecting_time, screen.convert_vector_to_screen)
        rifle.draw_image_representation(screen.screen, time, screen.convert_vector_to_screen)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            self._is_done = True

    def step_description(self):
        return "Tout est prêt! Parcourez le graphe avec votre souris pour voir la simulation"
