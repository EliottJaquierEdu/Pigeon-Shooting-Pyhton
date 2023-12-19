import math
from abc import ABC

from graph_line import GraphLine


class Rifle(GraphLine, ABC):
    def __init__(self, color, min_time, max_time, samples):
        super().__init__(color, min_time, max_time, samples)
        self.start_x = 5
        self.start_y = 2
        self.speed = 200
        self.angle = 30

    def x(self, t):
        wait = 0
        return self.start_x + math.cos(math.radians(self.angle)) * self.speed * (t - wait)

    def y(self, t):
        wait = 0
        return self.start_y + math.sin(math.radians(self.angle)) * self.speed * (t - wait)

    def wait_time(self, ap, vp, xpy):
        ac = math.radians(self.angle)
        vc = self.speed
        xcx = self.start_x
        xcy = self.start_y
        wait_minus = ((-0.10193679918451*((math.cos(ac)*vc-math.cos(ap)*vp)*math.sqrt(math.pow(math.cos(ac),2)(math.pow((math.sin(ap)),2)-19.62*(xcy-xpy))-2.*math.sin(ac)*math.cos(ac)*(math.sin(ap)*math.cos(ap)*vp-9.81*xcx)+math.pow((math.sin(ac)),2)*math.pow((math.cos(ap)),2)*math.pow(vp,2))-math.pow((math.cos(ac)),2)*math.sin(ap)*vc+(math.sin(ac)*math.cos(ap)*vc*vp+math.sin(ap)*math.cos(ap)*vp-9.81*xcx)*math.cos(ac)-math.sin(ac)*math.pow((math.cos(ap)),2)*math.pow(vp,2)))/(math.pow((math.cos(ac)),2)*vc))
        wait_plus = ((0.10193679918451*((math.cos(ac)*vc-math.cos(ap)*vp)*math.sqrt(math.pow(math.cos(ac),2)*(math.pow((math.sin(ap)),2)-19.62*(xcy-xpy))-2.*math.sin(ac)*math.cos(ac)*(math.sin(ap)*math.cos(ap)*vp-9.81*xcx)+math.pow((math.sin(ac)),2)*math.pow(math.cos(ap),2)*math.pow(vp,2))+math.pow((math.cos(ac)),2)*math.sin(ap)*vc-(math.sin(ac)*math.cos(ap)*vc*vp+math.sin(ap)*math.cos(ap)*vp-9.81*xcx)*math.cos(ac)+math.sin(ac)*math.pow((math.cos(ap)),2)*math.pow(vp,2)))/(math.pow((math.cos(ac)),2)*vc))
        return [wait_minus, wait_plus]