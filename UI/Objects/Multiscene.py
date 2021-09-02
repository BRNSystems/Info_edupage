import math
import pygame
from numpy import array as a
from Objects.Scene import Scene


class Multiscene(Scene):
    def __init__(self, width: float, height: float, scene_size: a):
        super().__init__(width, height, scene_size)

        self.subscenes = []
        self.subscenes_prepared = False

    def prepare_subscenes(self):

        for subscene in self.subscenes:
            subscene.multiscene = self
            subscene.subscene_size = subscene.screen_size
            subscene.resize_screen(self.to_ints((self.matrix @ subscene.subscene_size).tolist()), True)

        self.subscenes_prepared = True

    def redraw(self):
        if self.subscenes_prepared is False:
            self.prepare_subscenes()

        self.s_.fill(self.bg)

        for object_ in self.r_objects:
            object_.blit()

        rs = pygame.transform.scale(self.s_, self.screen_size)
        self.s.blit(rs, [0, 0])

        for scene in self.subscenes:
            scene.blit()

        for object_ in self.nr_objects:
            object_.blit()

        pygame.display.update()

    def resize_screen(self, new_screen_size, subscene=False):
        if self.subscenes_prepared is False:
            self.prepare_subscenes()

        self.screen_size = a(new_screen_size)
        self.matrix = a([
            [new_screen_size[0] / self.width, 0],
            [0, new_screen_size[1] / self.height]
        ])
        self.pd = abs(self.matrix[0, 0] * self.matrix[1, 1])  # positive determinant
        self.pd_ = math.sqrt(self.pd)

        if subscene is False:
            self.s = pygame.display.set_mode(new_screen_size)
        else:
            self.s = pygame.Surface(new_screen_size)

        self.resize_subscenes()

    def progress(self):
        self.progress_subscenes()

    def resize_subscenes(self):
        for subscene in self.subscenes:
            subscene.resize_screen(self.to_ints((self.matrix @ subscene.subscene_size).tolist()), True)

    def progress_subscenes(self):
        for subscene in self.subscenes:
            subscene.progress()

    @staticmethod
    def to_ints(iterable):
        for i in range(len(iterable)):
            iterable[i] = int(iterable[i])

        return iterable
