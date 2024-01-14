from abc import ABC

import pygame

from steps.step import Step
from ui.debug_bar import DebugBar


class SimulateTimeWithMouseStep(Step, ABC):
    def __init__(self, rifle, pigeon):
        super().__init__(rifle, pigeon)
        rifle.is_drawable = True
        pigeon.is_drawable = True
        self.debug_bar = DebugBar()

    def reset(self):
        super().reset()
        self.is_auto_simulating = False
        self.is_playing_audio = False
        self.time = 0
        self.intersecting_time = self.rifle.time_intersecting_with_pigeon(self.pigeon)
        self.rifle.wait_time = self.rifle.waiting_time_to_intersect(self.pigeon)

    def next_step(self):
        return None

    def update(self, screen, mouse_position, playtime):
        if self.is_done:
            return
        super().update(screen, mouse_position, playtime)
        mouse_position_vector_space = screen.convert_screen_to_vector(mouse_position)
        self.time = self.pigeon.t(mouse_position_vector_space[0])
        if self.is_auto_simulating:
            times = self.pigeon.time_when_zeros()
            landing = max(times[0], times[1])
            self.time = playtime % (landing + 2)

        if self.is_playing_audio:
            self.rifle.play_audio(self.time, playtime, 1 if self.is_auto_simulating else 20)

        self.rifle.is_points_drawn = self.debug_bar.is_visible
        self.pigeon.is_points_drawn = self.debug_bar.is_visible

        self.pigeon.draw_image_representation(screen.screen, self.time, self.intersecting_time,
                                              screen.convert_vector_to_screen)
        self.rifle.draw_image_representation(screen.screen, self.time, screen.convert_vector_to_screen)

    def on_hud(self, screen, width, height, draw_text_function, default_font, default_color):
        super().on_hud(screen, width, height, draw_text_function, default_font, default_color)
        self.debug_bar.draw(screen, draw_text_function, default_font, default_color, self.pigeon, self.rifle, self.time, self.intersecting_time, self.is_playing_audio, self.is_auto_simulating)

    def handle_event(self, event):
        super().handle_event(event)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.is_auto_simulating = not self.is_auto_simulating

        if event.type == pygame.KEYDOWN and event.key == pygame.K_i:
            self.debug_bar.is_visible = not self.debug_bar.is_visible

        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            self.is_playing_audio = not self.is_playing_audio

    def step_description(self):
        return "Tout est prêt! Parcourez le graphe avec votre souris pour voir la simulation et appuyez sur la touche 'i' pour voir plus d'infos."
