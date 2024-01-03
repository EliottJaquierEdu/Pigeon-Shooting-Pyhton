from abc import abstractmethod


class Step:
    def __init__(self):
        self._is_done = False
        self.previous_step = None

    @abstractmethod
    def update(self, screen, mouse_position, time, rifle, pigeon):
        pass

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
