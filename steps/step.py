from abc import abstractmethod


class Step:
    def __init__(self):
        self._is_done = False

    @abstractmethod
    def update(self, screen, mouse_position, mouse_buttons, rifle, pigeon):
        pass

    @abstractmethod
    def step_description(self):
        pass

    @abstractmethod
    def previous_step(self):
        pass

    @abstractmethod
    def next_step(self):
        pass

    @property
    def is_done(self):
        return self._is_done
