from abc import abstractmethod

import pygame


class Step:
    def __init__(self, rifle, pigeon):
        self._is_done = False
        self.previous_step = None
        self.rifle = rifle
        self.pigeon = pigeon
        self.last_mouse_position = []

    def update(self, screen, mouse_position, time):
        self.last_mouse_position = mouse_position

    def on_hud(self, surface, width, height, draw_text_function, default_font, default_color):
        draw_text_function(surface, default_font, self.step_description(), default_color, width / 2, 48)

    @abstractmethod
    def handle_event(self, event):
        pass

    @abstractmethod
    def step_description(self):
        pass

    @abstractmethod
    def next_step(self):
        pass

    @property
    def is_done(self):
        return self._is_done
