import pygame.transform
from Objects.Screen import Screen
from numpy import array as a


class Scene(Screen):
    def __init__(self, width: float, height: float, font_size: int, scene_size: a, bg=(60, 60, 60)):
        super().__init__(width, height, font_size, scene_size)

        self.bg = bg
        self.r_objects = []  # resizable Objects
        self.nr_objects = []  # non-resizable Objects

    def redraw(self):
        self.s_.fill(self.bg)

        for object_ in self.r_objects:
            object_.blit()

        rs = pygame.transform.scale(self.s_, self.screen_size)
        self.s.blit(rs, [0, 0])

        for object_ in self.nr_objects:
            object_.blit()

        pygame.display.update()
