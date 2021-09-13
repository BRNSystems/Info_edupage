import copy
import math
import pygame
from numpy import array as a
from UI.Objects.Scene import Scene


class Multiscene(Scene):

    object_type = "multiscene"

    def __init__(self, width: float, height: float, scene_size: a):
        super().__init__(width, height, scene_size)

        self.subscenes = []
        self.subscenes_prepared = False

    def prepare_subscenes(self):

        for subscene in self.subscenes:
            subscene.multiscene = self
            subscene.subscene_size = subscene.screen_size
            subscene.resize_screen(self.to_ints((self.matrix @ subscene.subscene_size).tolist()), True)

        self.s = pygame.display.set_mode(self.screen_size)

        self.subscenes_prepared = True

    def light_update(self):
        for subscene in self.subscenes:
            subscene.light_update()

        for object_ in self.l_objects:
            object_.update()
            object_.blit(True)

        pygame.display.update()

    def update(self):
        if self.subscenes_prepared is False:
            self.prepare_subscenes()

        self.s_.fill(self.bg)

        for object_ in self.l_objects:
            object_.update()

        for object_ in self.r_objects:
            object_.blit()

        rs = pygame.transform.scale(self.s_, self.screen_size)
        self.s.blit(rs, [0, 0])

        for scene in self.subscenes:
            scene.blit()

        for object_ in self.nr_objects:
            object_.blit()

        for object_ in self.d_objects:
            object_.progress()

        for object_ in self.c_objects:
            object_.input(self.mouse_pos, self.clicked)

        pygame.display.update()

    def resize_screen(self, new_screen_size, subscene=False):
        if self.subscenes_prepared is False:
            self.prepare_subscenes()

        self.screen_size = a(new_screen_size)
        self.matrix = a([
            [new_screen_size[0] / self.width, 0],
            [0, new_screen_size[1] / self.height]
        ])
        self.inverse_matrix = a([
            [1 / self.matrix[0, 0], 0],
            [0, 1 / self.matrix[1, 1]]
        ])
        self.pd = abs(self.matrix[0, 0] * self.matrix[1, 1])  # positive determinant
        self.pd_ = math.sqrt(self.pd)

        if subscene is False:
            self.s = pygame.display.set_mode(new_screen_size)
        else:
            self.s = pygame.Surface(new_screen_size)

        self.resize_subscenes()

    def update_mouse_events(self, mouse_pos, clicked):
        mouse_pos = a(mouse_pos)
        self.mouse_pos = self.inverse_matrix @ mouse_pos
        self.clicked = clicked

        for subscene in self.subscenes:
            subscene.mouse_pos = (subscene.inverse_matrix @ (mouse_pos - (self.matrix @ subscene.position)))
            subscene.clicked = clicked

    def progress(self):
        self.progress_subscenes()

    def resize_subscenes(self):
        for subscene in self.subscenes:
            subscene.resize_screen(self.to_ints((self.matrix @ subscene.subscene_size).tolist()), True)

    def progress_subscenes(self):
        for subscene in self.subscenes:
            subscene.progress()

    def get_i_objects(self):
        i_objects = [[copy.copy(self.i_objects), self.mouse_pos]]

        for subscene in self.subscenes:
            i_objects += subscene.get_i_objects()

        return i_objects

    @staticmethod
    def to_ints(iterable):
        for i in range(len(iterable)):
            iterable[i] = int(iterable[i])

        return iterable
