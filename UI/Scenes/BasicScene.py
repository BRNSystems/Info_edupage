from UI.Objects.Scene import Scene
from numpy import array as a

from UI.Objects.nr_objects.Ellipse import Ellipse
from UI.Objects.nr_objects.Circle import Circle
from UI.Objects.nr_objects.EquilateralTriangle import EquilateralTriangle
from UI.Objects.nr_objects.Image import Image
from UI.Objects.nr_objects.Line import Line
from UI.Objects.nr_objects.Text import Text
from UI.Objects.r_objects.Rect import Rect


class BasicScene(Scene):
    def __init__(self, scene_size: a, bg=(60, 60, 60)):

        self.s__size = [600, 400]

        super().__init__(self.s__size[0], self.s__size[1], scene_size, bg)

        r0 = Rect(a([0, 0]), a([200, 200]), (160, 160, 160), self)
        self.r_objects.append(r0)

        l0 = Line(a([100, 300]), a([500, 100]), 3, (255, 100, 100), self)
        self.nr_objects.append(l0)

        c0 = Circle(a([400, 200]), 40, (100, 100, 255), self)
        self.nr_objects.append(c0)

        e0 = Ellipse(a([150, 360]), 60, 20, (100, 255, 100), self)
        self.nr_objects.append(e0)

        t0 = Text(a([100, 50]), "hello world!", 26, (200, 200, 200), self)
        self.nr_objects.append(t0)

        i0 = Image(a([200, 0]), 0.8, "test.png", self)
        self.nr_objects.append(i0)

        t0 = EquilateralTriangle(a([500, 300]), 30, 1, (250, 250, 150), self)
        self.nr_objects.append(t0)
