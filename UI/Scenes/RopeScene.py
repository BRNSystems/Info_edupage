from Objects.Scene import Scene
from numpy import array as a
import pygame

from UI.Objects.nr_objects.dynamic_objects.Rope import Rope
from UI.Objects.nr_objects.controllable_objects.RopeInteractiveDot import RopeInteractiveDot


class RopeScene(Scene):
    def __init__(self, scene_size, bg=(60, 60, 60)):

        s__size = [600, 400]

        super().__init__(s__size[0], s__size[1], scene_size, bg)

        r0 = Rope(a([300, 50]), 200, 40, 2, 2, self)
        self.nrd_objects.append(r0)

        rd0 = RopeInteractiveDot(a([100, 100]), 10, (100, 255, 100), 20, 100, self)
        self.nrc_objects.append(rd0)

        pygame.mouse.set_visible(False)
