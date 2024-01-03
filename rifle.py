import math
from abc import ABC

import pygame.mixer

from object_graph_line import ObjectGraphLine


class Rifle(ObjectGraphLine, ABC):
    def __init__(self, color, line_width,  samples):
        super().__init__(color, line_width, 0, 1, samples)
        self.start_x = 5
        self.start_y = 2
        self.speed = 200
        self.angle = 30

        self.shoot_t = 0
        self.last_t = 0
        self.last_raw_game_time = 0
        pygame.mixer.init(frequency=44100)
        self.shoot_audio = pygame.mixer.Sound("res/shot.wav")
        self.shoot_audio_inv = pygame.mixer.Sound("res/shot_inv.wav")
        self.newsnd = self.shoot_audio

    def x(self, t):
        return self.start_x + math.cos(math.radians(self.angle)) * self.speed * (t - self.shoot_t)

    def y(self, t):
        return self.start_y + math.sin(math.radians(self.angle)) * self.speed * (t - self.shoot_t)

    def play_audio(self,t,raw_game_time):
        deltaTime = raw_game_time - self.last_raw_game_time
        t = t - self.shoot_t
        if(t == self.last_t): return

        if (t > 0) and (t < self.shoot_audio.get_length()):
            sample = 0.05
            if(deltaTime > sample):
                self.last_raw_game_time = self.last_raw_game_time + sample

                offset = int(t*44100) if t > self.last_t else int((self.shoot_audio_inv.get_length()-t)*44100)
                duration = offset+int(44100*(sample+0.01))
                samps = pygame.sndarray.samples(self.shoot_audio if t > self.last_t else self.shoot_audio_inv)[offset:duration]
                #self.newsnd.stop()
                self.newsnd = pygame.sndarray.make_sound(samps)
                self.newsnd.play()

        self.last_t = t

    def get_lines(self, space_conversion_fn, force_refresh=False):
        self.min_time = self.shoot_t
        self.max_time = self.shoot_t + 1
        return super().get_lines(space_conversion_fn, force_refresh)

    def wait_time(self, ap, vp, xpy):
        ac = math.radians(self.angle)
        vc = self.speed
        xcx = self.start_x
        xcy = self.start_y
        wait_minus = ((-0.10193679918451*((math.cos(ac)*vc-math.cos(ap)*vp)*math.sqrt(math.pow(math.cos(ac),2)*(math.pow((math.sin(ap)),2)-19.62*(xcy-xpy))-2.*math.sin(ac)*math.cos(ac)*(math.sin(ap)*math.cos(ap)*vp-9.81*xcx)+math.pow((math.sin(ac)),2)*math.pow((math.cos(ap)),2)*math.pow(vp,2))-math.pow((math.cos(ac)),2)*math.sin(ap)*vc+(math.sin(ac)*math.cos(ap)*vc*vp+math.sin(ap)*math.cos(ap)*vp-9.81*xcx)*math.cos(ac)-math.sin(ac)*math.pow((math.cos(ap)),2)*math.pow(vp,2)))/(math.pow((math.cos(ac)),2)*vc))
        wait_plus = ((0.10193679918451*((math.cos(ac)*vc-math.cos(ap)*vp)*math.sqrt(math.pow(math.cos(ac),2)*(math.pow((math.sin(ap)),2)-19.62*(xcy-xpy))-2.*math.sin(ac)*math.cos(ac)*(math.sin(ap)*math.cos(ap)*vp-9.81*xcx)+math.pow((math.sin(ac)),2)*math.pow(math.cos(ap),2)*math.pow(vp,2))+math.pow((math.cos(ac)),2)*math.sin(ap)*vc-(math.sin(ac)*math.cos(ap)*vc*vp+math.sin(ap)*math.cos(ap)*vp-9.81*xcx)*math.cos(ac)+math.sin(ac)*math.pow((math.cos(ap)),2)*math.pow(vp,2)))/(math.pow((math.cos(ac)),2)*vc))
        return [wait_minus, wait_plus]