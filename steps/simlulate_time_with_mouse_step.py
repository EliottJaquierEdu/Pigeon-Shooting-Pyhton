import math
from abc import ABC

import pygame

from steps.step import Step


class SimulateTimeWithMouseStep(Step, ABC):
    def __init__(self, rifle, pigeon):
        super().__init__(rifle, pigeon)
        self.is_auto_simulating = False

    def next_step(self):
        return None

    def update(self, screen, mouse_position, playtime):
        if self.is_done:
            return
        mouse_position_vector_space = screen.convert_screen_to_vector(mouse_position)
        time = self.pigeon.t(mouse_position_vector_space[0])
        if self.is_auto_simulating:
            times = self.pigeon.time_when_zeros()
            landing = max(times[0], times[1])
            time = playtime % (landing+1)
        self.rifle.play_audio(time, playtime, 1 if self.is_auto_simulating else 20)
        intersecting_time = self.rifle.time_intersecting_with_pigeon(self.pigeon)
        self.rifle.wait_time = self.rifle.waiting_time_to_intersect(self.pigeon)
        self.pigeon.draw_image_representation(screen.screen, time, intersecting_time, screen.convert_vector_to_screen)
        self.rifle.draw_image_representation(screen.screen, time, screen.convert_vector_to_screen)

    def on_hud(self, surface, width, height, draw_text_function):
        super().on_hud(surface, width, height, draw_text_function)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.is_auto_simulating = not self.is_auto_simulating

    def step_description(self):
        return "Tout est prêt! Parcourez le graphe avec votre souris pour voir la simulation"
