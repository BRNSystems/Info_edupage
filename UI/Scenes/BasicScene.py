from Objects.Scene import Scene
from Objects.r_objects import *
from numpy import array as a
import numpy as np

from UI.Objects.r_objects.Rect import Rect


class BasicScene(Scene):
    def __init__(self, font_size: int, screen_size: a, bg=(60, 60, 60)):

        s__size = [600, 400]

        super().__init__(s__size[0], s__size[1], font_size, screen_size, bg)

        r0 = Rect(a([0, 0]), a([200, 200]), (160, 160, 160), self)
        self.r_objects.append(r0)
