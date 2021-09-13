from TuGUI.Objects.Scene import Scene
from numpy import array as a
import pygame

from TuGUI.Objects.nr_objects.dynamic_objects.Rope import Rope
from TuGUI.Objects.nr_objects.controllable_objects.RopeInteractiveDot import RopeInteractiveDot


class RopeScene(Scene):
    def __init__(self, scene_size, bg=(60, 60, 60)):

        self.s__size = [600, 400]

        super().__init__(self.s__size[0], self.s__size[1], scene_size, bg)

        r0 = Rope(a([300, 50]), 200, 20, 2, 2, self)

        rd0 = RopeInteractiveDot(a([0, 0]), 10, (100, 255, 100), 20, 100, self)

        self.sort_objects(r0, rd0)

        pygame.mouse.set_visible(False)
