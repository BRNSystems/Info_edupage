from numpy import array as a

from UI.Objects.Multiscene import Multiscene
from UI.Objects.nr_objects.Line import Line
from UI.Objects.nr_objects.controllable_objects.RopeInteractiveDot import RopeInteractiveDot
from UI.Scenes.RopeScene import RopeScene


class RopeMultiscene(Multiscene):
    def __init__(self, scene_size):

        self.s__size = [800, 400]

        super().__init__(self.s__size[0], self.s__size[1], scene_size)

        s0 = RopeScene([200, 400])
        self.subscenes.append(s0)

        s1 = RopeScene([600, 400])
        s1.position = a([200, 0])
        self.subscenes.append(s1)

        l0 = Line(a([200, 0]), a([200, 400]), 10, (255, 100, 100), self)
        self.nr_objects.append(l0)

        rd0 = RopeInteractiveDot(a([0, 0]), 10, (100, 255, 100), 20, 100, self)
        #self.nrc_objects.append(rd0)

        self.i = 0

    def progress(self):
        if self.i == 1:
            self.subscenes[0].subscene_size[0] += 2
            self.subscenes[1].subscene_size[0] -= 2
            self.subscenes[1].position[0] += 2

            self.nr_objects[0].a[0] += 2
            self.nr_objects[0].b[0] += 2

            self.resize_subscenes()
            self.i = 0
        else:
            self.i += 1