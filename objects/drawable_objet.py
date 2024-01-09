from abc import abstractmethod


class DrawableObject:
    def __init__(self):
        self.is_drawable = True

    @abstractmethod
    def draw(self, screen, width, height, space_conversion_fn):
        pass
