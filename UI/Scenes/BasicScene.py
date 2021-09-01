from Objects.Scene import Scene
from Objects.r_objects import *
from numpy import array as a
import numpy as np

from UI.Objects.nr_objects.Ellipse import Ellipse
from UI.Objects.nr_objects.Circle import Circle
from UI.Objects.nr_objects.Line import Line
from UI.Objects.r_objects.Rect import Rect


class BasicScene(Scene):
    def __init__(self, font_size: int, scene_size: a, bg=(60, 60, 60)):

        s__size = [600, 400]

        super().__init__(s__size[0], s__size[1], font_size, scene_size, bg)

        r0 = Rect(a([0, 0]), a([200, 200]), (160, 160, 160), self)
        self.r_objects.append(r0)

        l0 = Line(a([100, 300]), a([500, 100]), 3, (255, 100, 100), self)
        self.nr_objects.append(l0)

        c0 = Circle(a([400, 200]), 40, (100, 100, 255), self)
        self.nr_objects.append(c0)

        e0 = Ellipse(a([150, 360]), 60, 20, (100, 255, 100), self)
        self.nr_objects.append(e0)
