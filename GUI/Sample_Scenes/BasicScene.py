from GUI.Objects.Scene import Scene
from numpy import array as a

from GUI.Objects.nr_objects.Ellipse import Ellipse
from GUI.Objects.nr_objects.Circle import Circle
from GUI.Objects.nr_objects.EquilateralTriangle import EquilateralTriangle
from GUI.Objects.nr_objects.Image import Image
from GUI.Objects.nr_objects.Line import Line
from GUI.Objects.nr_objects.Text import Text
from GUI.Objects.r_objects.Rect import Rect


class BasicScene(Scene):
    def __init__(self, scene_size: a, bg=(60, 60, 60)):

        self.s__size = [600, 400]

        super().__init__(self.s__size[0], self.s__size[1], scene_size, bg)

        r0 = Rect(a([0, 0]), a([200, 200]), (160, 160, 160), self)

        l0 = Line(a([100, 300]), a([500, 100]), 3, (255, 100, 100), self)

        c0 = Circle(a([400, 200]), 40, (100, 100, 255), self)

        e0 = Ellipse(a([150, 360]), 60, 20, (100, 255, 100), self)

        t0 = Text(a([100, 50]), "hello world!", 26, (200, 200, 200), self)

        i0 = Image(a([200, 0]), 0.8, "sample_image.png", self)

        triangle0 = EquilateralTriangle(a([500, 300]), 30, 1, (250, 250, 150), self)

        self.sort_objects(r0, l0, c0, e0, t0, i0, triangle0)
