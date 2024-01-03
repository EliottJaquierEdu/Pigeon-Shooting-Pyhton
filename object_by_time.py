from abc import abstractmethod


class ObjectByTime:

    @abstractmethod
    def x(self, t):
        pass

    @abstractmethod
    def y(self, t):
        pass

    @abstractmethod
    def draw_image_representation(self, display, t, space_conversion_fn):
        pass
