from abc import abstractmethod, ABC

import utils
from object_by_time import ObjectByTime


class ObjectGraphLine(ObjectByTime, ABC):
    def __init__(self, color, min_time, max_time, samples):
        self._min_time = min_time
        self._max_time = max_time
        self._samples = samples
        self.color = color

        self._cached_line_points = []
        self._need_refresh = True

    @property
    def min_time(self):
        return self._min_time

    @min_time.setter
    def min_time(self, new_min_time):
        self._min_time = new_min_time
        self._need_refresh = True

    @property
    def max_time(self):
        return self._max_time

    @max_time.setter
    def max_time(self, new_max_time):
        self._max_time = new_max_time
        self._need_refresh = True

    @property
    def samples(self):
        return self._samples

    @samples.setter
    def samples(self, new_samples):
        self._samples = new_samples
        self._need_refresh = True

    def get_point(self, t, space_conversion_fn):
        return space_conversion_fn([self.x(t), self.y(t)])

    def get_lines(self, space_conversion_fn, force_refresh=False):
        if not (self._need_refresh or force_refresh):
            self._need_refresh = False
            return self._cached_line_points

        self._cached_line_points.clear()
        for i in range(self._samples + 1):
            percentage = i / self._samples
            time = utils.lerp(self._min_time, self._max_time, percentage)
            point = self.get_point(time, space_conversion_fn)
            self._cached_line_points.append(point)
        return self._cached_line_points
