from GUI.Objects.Scene import Scene
from numpy import array as a

from GUI.Objects.nr_objects.light_objects.LuminousCircleEffect import LuminousCircleEffect


class LuminousCircleEffectScene(Scene):
    def __init__(self, screen_size, bg=(60, 60, 60)):

        s__size = [600, 400]

        super().__init__(*s__size, screen_size, bg)

        lce0 = LuminousCircleEffect(a([300, 200]), 100, (80, 120, 80), self, circles_n=60)

        self.sort_objects(lce0)
