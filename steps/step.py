from abc import abstractmethod


class Step:
    def __init__(self, rifle, pigeon):
        self._is_done = False
        self.previous_step = None
        self.rifle = rifle
        self.pigeon = pigeon

    @abstractmethod
    def update(self, screen, mouse_position, time):
        pass

    def on_hud(self, surface, width, height, draw_text_function):
        draw_text_function(surface, self.step_description(), width/2, 48)

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
