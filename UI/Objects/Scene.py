import pygame.transform
from UI.Objects.Screen import Screen
from numpy import array as a


class Scene(Screen):
    def __init__(self, width: float, height: float, scene_size: a, bg=(60, 60, 60)):
        super().__init__(width, height, scene_size)

        self.bg = bg
        self.r_objects = []  # resizable Objects
        self.nr_objects = []  # non-rescalable Objects

        self.nrd_objects = []  # non-rescalable dynamic Objects
        self.nrc_objects = []  # non-rescalable controllable Objects

        self.i_objects = []  # interactive Objects

        self.position = a([0, 0])
        self.multiscene = None

        self.mouse_pos = a([0, 0])
        self.clicked = False

    def update(self):
        self.s_.fill(self.bg)

        for object_ in self.r_objects:
            object_.blit()

        rs = pygame.transform.scale(self.s_, self.screen_size)
        self.s.blit(rs, [0, 0])

        for object_ in self.nr_objects:
            object_.blit()

        for object_ in self.nrd_objects:
            object_.blit()
            object_.progress()

        for object_ in self.nrc_objects:
            object_.blit()
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
        return self.i_objects
