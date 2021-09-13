from numpy import array as a

from GUI.Objects.Multiscene import Multiscene
from GUI.Objects.nr_objects.Line import Line
from GUI.Sample_Scenes.RopeScene import RopeScene


class RopeMultiscene(Multiscene):
    def __init__(self, scene_size):

        self.s__size = [800, 400]

        super().__init__(self.s__size[0], self.s__size[1], scene_size)

        s0 = RopeScene([200, 400])

        s1 = RopeScene([600, 400])
        s1.position = a([200, 0])

        l0 = Line(a([200, 0]), a([200, 400]), 10, (255, 100, 100), self)

        self.sort_objects(s0, s1, l0)

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
