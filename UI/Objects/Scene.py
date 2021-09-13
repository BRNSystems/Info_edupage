import pygame.transform
from UI.Objects.Screen import Screen
from numpy import array as a
import numpy as np


class Scene(Screen):

    object_type = "scene"

    def __init__(self, width: float, height: float, scene_size: a, bg=(60, 60, 60)):
        super().__init__(width, height, scene_size)

        self.bg = bg
        self.r_objects = []  # resizable Objects
        self.nr_objects = []  # non-rescalable Objects

        self.d_objects = []  # dynamic Objects
        self.c_objects = []  # controllable Objects
        self.i_objects = []  # interactive Objects
        self.l_objects = []  # light Objects

        self.position = a([0, 0])
        self.multiscene = None

        self.mouse_pos = a([0, 0])
        self.clicked = False

    def light_update(self):
        for object_ in self.l_objects:
            object_.update()
            object_.blit(True)

        pygame.display.update()

    def update(self):
        self.s_.fill(self.bg)

        for object_ in self.l_objects:
            object_.update()

        for object_ in self.r_objects:
            object_.blit()

        rs = pygame.transform.scale(self.s_, self.screen_size)
        self.s.blit(rs, [0, 0])

        for object_ in self.nr_objects:
            object_.blit()

        for object_ in self.d_objects:
            object_.progress()

        for object_ in self.c_objects:
            object_.input(self.mouse_pos, self.clicked)

        pygame.display.update()

    def update_mouse_events(self, mouse_pos, clicked):
        self.mouse_pos = self.inverse_matrix @ a(mouse_pos)
        self.clicked = clicked

    def blit(self):
        self.update()
        self.multiscene.s.blit(self.s, self.multiscene.matrix @ self.position)

    def progress(self):
        pass

    def get_i_objects(self):
        return [[self.i_objects, self.mouse_pos]]

    def get_info_for_light_objects(self, position):
        s = self
        positions = [position]
        matrices = [self.matrix]

        while s.multiscene is not None:
            positions.append(s.position)
            s = s.multiscene
            matrices.append(s.matrix)

        transformed_position = a([0., 0.])
        for p, m in zip(positions, matrices):
            transformed_position += a(m @ p)

        return s.s, transformed_position

    def sort_objects(self, *args):
        for object_ in args:
            for object_tag in object_.object_type.split("_"):
                if object_tag == "r":
                    self.r_objects.append(object_)
                elif object_tag == "nr":
                    self.nr_objects.append(object_)
                elif object_tag == "d":
                    self.d_objects.append(object_)
                elif object_tag == "c":
                    self.c_objects.append(object_)
                elif object_tag == "i":
                    self.i_objects.append(object_)
                elif object_tag == "l":
                    self.l_objects.append(object_)
                elif object_tag in ["scene", "multiscene"]:
                    if self.object_type == "multiscene":
                        self.subscenes.append(object_)
                    else:
                        raise ValueError("Scene/Multiscene object encountered in scene.sort_objects()\n"
                                         "Please use Multiscene for this purpose.")
