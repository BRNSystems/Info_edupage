import pygame.transform
from Objects.Screen import Screen
from numpy import array as a


class Scene(Screen):
    def __init__(self, width: float, height: float, scene_size: a, bg=(60, 60, 60)):
        super().__init__(width, height, scene_size)

        self.bg = bg
        self.r_objects = []  # resizable Objects
        self.nr_objects = []  # non-rescalable Objects

        self.position = a([0, 0])
        self.multiscene = None

    def redraw(self):
        self.s_.fill(self.bg)

        for object_ in self.r_objects:
            object_.blit()

        rs = pygame.transform.scale(self.s_, self.screen_size)
        self.s.blit(rs, [0, 0])

        for object_ in self.nr_objects:
            object_.blit()

        pygame.display.update()

    def blit(self):
        self.redraw()
        self.multiscene.s.blit(self.s, self.multiscene.matrix @ self.position)

    def progress(self):
        pass
