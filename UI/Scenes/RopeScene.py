from Objects.Scene import Scene
from numpy import array as a

from UI.Objects.nr_objects.dynamic_objects.Rope import Rope
from UI.Objects.nr_objects.controllable_objects.RopeInteractiveDot import RopeInteractiveDot


class RopeScene(Scene):
    def __init__(self, scene_size, bg=(60, 60, 60)):

        s__size = [600, 400]

        super().__init__(s__size[0], s__size[1], scene_size, bg)

        r0 = Rope(a([300, 50]), 400, 20, 2, 2, self, gravity=5)
        self.nrd_objects.append(r0)

        rd0 = RopeInteractiveDot(a([100, 100]), 20, (100, 255, 100), 5, 100, self)
        self.nrc_objects.append(rd0)
