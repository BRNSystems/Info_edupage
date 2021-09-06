from UI.Objects.Multiscene import Multiscene
from UI.Scenes.BasicMultiscene import BasicMultiscene
from numpy import array as a

from UI.Objects.nr_objects.Line import Line


class MultisceneInMultiscene(Multiscene):
    def __init__(self, scene_size):
        self.s__size = [600, 800]

        super().__init__(self.s__size[0], self.s__size[1], scene_size)

        ms0 = BasicMultiscene([600, 400])

        ms1 = BasicMultiscene([600, 400])
        ms1.position = a([0, 400])

        l0 = Line(a([0, 400]), a([600, 400]), 12, (100, 100, 255), self)

        self.sort_objects(ms0, ms1, l0)

        self.i = 0

    def progress(self):
        self.progress_subscenes()

        if self.i == 1:
            self.subscenes[0].subscene_size[1] += 1
            self.subscenes[1].subscene_size[1] -= 1
            self.subscenes[1].position[1] += 1

            self.nr_objects[0].a[1] += 1
            self.nr_objects[0].b[1] += 1

            self.resize_subscenes()
            self.i = 0
        else:
            self.i += 1


