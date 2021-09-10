from UI.Objects.Multiscene import Multiscene
from UI.Objects.nr_objects.light_objects.LuminousCircleEffect import LuminousCircleEffect
from UI.Scenes.Sample_Scenes.LuminousCircleEffectScene import LuminousCircleEffectScene
from numpy import array as a

from UI.Objects.nr_objects.Line import Line


class LuminousCircleEffectMultiscene(Multiscene):
    def __init__(self, scene_size):

        self.s__size = [600, 400]

        super().__init__(self.s__size[0], self.s__size[1], scene_size)

        s0 = LuminousCircleEffectScene([200, 400])

        s1 = LuminousCircleEffectScene([400, 400])
        s1.position = a([200, 0])

        l0 = Line(a([200, 0]), a([200, 400]), 10, (255, 100, 100), self)

        lce0 = LuminousCircleEffect(a([200, 320]), 60, (255, 100, 100), self)

        self.sort_objects(s0, s1, l0, lce0)

        self.i = 0

    def progress(self):
        if self.i == 1:
            self.subscenes[0].subscene_size[0] += 1
            self.subscenes[1].subscene_size[0] -= 1
            self.subscenes[1].position[0] += 1

            self.nr_objects[0].a[0] += 1
            self.nr_objects[0].b[0] += 1

            self.l_objects[0].position[0] += 1

            self.resize_subscenes()
            self.i = 0
        else:
            self.i += 1
