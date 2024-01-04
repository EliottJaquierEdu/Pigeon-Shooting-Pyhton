import math
from abc import ABC

import pygame.mixer

from object_graph_line import ObjectGraphLine


class Rifle(ObjectGraphLine, ABC):
    def __init__(self, color, line_width, samples):
        super().__init__(color, line_width, 0, 1, samples)
        self.start_x = 5
        self.start_y = 2
        self.speed = 200
        self.angle = 30

        self.wait_time = 0
        self.last_t = 0
        self.last_raw_game_time = 0
        self.image = pygame.image.load("res/bullet.png")
        self.shoot_audio = pygame.mixer.Sound("res/shot.wav")
        self.shoot_audio_inv = pygame.mixer.Sound("res/shot_inv.wav")
        self.newsnd = self.shoot_audio

    def x(self, t):
        return self.start_x + math.cos(math.radians(self.angle)) * self.speed * (t - self.wait_time)

    def y(self, t):
        return self.start_y + math.sin(math.radians(self.angle)) * self.speed * (t - self.wait_time)

    def get_point(self, t, space_conversion_fn):
        if t < self.wait_time:
            t = self.wait_time
        return super().get_point(t,space_conversion_fn)

    def play_audio(self, t, raw_game_time):
        deltaTime = raw_game_time - self.last_raw_game_time
        t = t - self.wait_time
        if (t == self.last_t): return

        if (t > 0) and (t < self.shoot_audio.get_length()):
            sample = 0.05
            if (deltaTime > sample):
                self.last_raw_game_time = self.last_raw_game_time + sample

                offset = int(t * 44100) if t > self.last_t else int((self.shoot_audio_inv.get_length() - t) * 44100)
                duration = offset + int(44100 * (sample + 0.01))
                samps = pygame.sndarray.samples(self.shoot_audio if t > self.last_t else self.shoot_audio_inv)[
                        offset:duration]
                # self.newsnd.stop()
                self.newsnd = pygame.sndarray.make_sound(samps)
                self.newsnd.play()

        self.last_t = t

    def get_lines(self, space_conversion_fn, force_refresh=False):
        self.min_time = self.wait_time
        self.max_time = self.wait_time + 1
        return super().get_lines(space_conversion_fn, force_refresh)

    def time_intersecting_with_pigeon(self, pigeon):
        sx = self.start_x
        sy = self.start_y
        sa = math.radians(self.angle)
        sv = self.speed

        pa = math.radians(pigeon.angle)
        py = pigeon.start_y
        pv = pigeon.speed

        t_plus = ((0.101937 * (math.sqrt(
            (math.cos(pa)) ** (2) * pv ** (2) * (math.sin(sa)) ** (2) - 2. * math.sin(pa) * math.cos(pa) * pv ** (
                2) * math.sin(sa) * math.cos(sa) + ((math.sin(pa)) ** (2) * pv ** (2) * math.cos(sa) + 19.62 * (
                    py * math.cos(sa) - math.cos(sa) * sy + math.sin(sa) * sx)) * math.cos(sa)) * abs(
            math.cos(pa) * pv - math.cos(sa) * sv) - ((math.cos(pa)) ** (2) * pv * math.sin(sa) - (
                math.sin(pa) * pv + math.sin(sa) * sv) * math.cos(pa) * math.cos(sa) + math.sin(pa) * (
                                                          math.cos(sa)) ** (2) * sv) * pv)) / (
                          (math.cos(pa) * pv - math.cos(sa) * sv) * math.cos(sa)))

        t_min = ((-0.101937 * (math.sqrt(
            (math.cos(pa)) ** (2) * pv ** (2) * (math.sin(sa)) ** (2) - 2. * math.sin(pa) * math.cos(pa) * pv ** (
                2) * math.sin(sa) * math.cos(sa) + ((math.sin(pa)) ** (2) * pv ** (2) * math.cos(sa) + 19.62 * (
                    py * math.cos(sa) - math.cos(sa) * sy + math.sin(sa) * sx)) * math.cos(sa)) * abs(
            math.cos(pa) * pv - math.cos(sa) * sv) + ((math.cos(pa)) ** (2) * pv * math.sin(sa) - (
                math.sin(pa) * pv + math.sin(sa) * sv) * math.cos(pa) * math.cos(sa) + math.sin(pa) * (
                                                          math.cos(sa)) ** (2) * sv) * pv)) / (
                         (math.cos(pa) * pv - math.cos(sa) * sv) * math.cos(sa)))

        return max(t_plus, t_min) if self.angle < 90 else min(t_plus, t_min)

    def waiting_time_to_intersect(self, pigeon):
        sx = self.start_x
        sy = self.start_y
        sa = math.radians(self.angle)
        sv = self.speed

        pa = math.radians(pigeon.angle)
        py = pigeon.start_y
        pv = pigeon.speed

        wait_min = ((-0.101937 * (math.sqrt((math.cos(pa)) ** (2) * pv ** (2) * (math.sin(sa)) ** (2) - 2 * math.sin(
            pa) * math.cos(pa) * pv ** (2) * math.sin(sa) * math.cos(sa) + (
                                                    (math.sin(pa)) ** (2) * pv ** (2) * math.cos(sa) + 19.62 * (
                                                    py * math.cos(sa) - math.cos(sa) * sy + math.sin(
                                                sa) * sx)) * math.cos(sa)) * abs(
            math.cos(pa) * pv - math.cos(sa) * sv) - (math.cos(pa)) ** (2) * pv ** (2) * math.sin(sa) + (math.sin(
            pa) * pv + math.sin(sa) * sv) * math.cos(pa) * pv * math.cos(sa) - (math.sin(pa) * pv * math.cos(
            sa) * sv + 9.81 * sx) * math.cos(sa))) / ((math.cos(sa)) ** (2) * sv))
        wait_plus = (+(0.101937 * (math.sqrt(
            (math.cos(pa)) ** (2) * pv ** (2) * (math.sin(sa)) ** (2) - 2 * math.sin(pa) * math.cos(pa) * pv ** (
                2) * math.sin(sa) * math.cos(sa) + ((math.sin(pa)) ** (2) * pv ** (2) * math.cos(sa) + 19.62 * (
                    py * math.cos(sa) - math.cos(sa) * sy + math.sin(sa) * sx)) * math.cos(sa)) * abs(
            math.cos(pa) * pv - math.cos(sa) * sv) + (math.cos(pa)) ** (2) * pv ** (2) * math.sin(sa) - (
                                           math.sin(pa) * pv + math.sin(sa) * sv) * math.cos(pa) * pv * math.cos(sa) + (
                                           math.sin(pa) * pv * math.cos(sa) * sv + 9.81 * sx) * math.cos(sa))) / (
                             (math.cos(sa)) ** (2) * sv))

        return max(wait_min, wait_plus) if self.angle < 90 else min(wait_min, wait_plus)

    def draw_image_representation(self, display, t, space_conversion_fn):
        points = self.get_point(t, space_conversion_fn)
        points[0] = points[0] - (self.image.get_width() / 2)
        points[1] = points[1] - (self.image.get_height() / 2)
        display.blit(self.image, points)
