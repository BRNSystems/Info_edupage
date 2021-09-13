from numpy import array as a
import numpy as np
import pygame
import copy


class Image:

    object_type = "nr"

    def __init__(self, center, scalar, path, scene):
        self.center = center
        self.scalar = scalar
        self.path = path
        self.scene = scene
        self.pd_ = self.scene.pd_

        self.image = pygame.image.load(self.path).convert()
        self.image = pygame.transform.scale(self.image,
                                            self.to_ints((a(self.image.get_size()) * self.scalar).tolist()))

        self.size = a(self.image.get_size(), dtype=np.float64)
        self.sides_ratio = self.size[0] / self.size[1]

        self.rescaled_size = copy.copy(self.size)
        if self.scene.matrix[1, 1] - self.scene.matrix[0, 0] / self.sides_ratio >= 0:
            self.rescaled_size *= self.scene.matrix[0, 0]
        else:
            self.rescaled_size *= self.scene.matrix[1, 1]

        self.rescaled_image = pygame.transform.scale(self.image, self.to_ints((self.size * self.pd_).tolist()))

    def blit(self):

        if self.pd_ != self.scene.pd_:
            self.pd_ = self.scene.pd_
            self.rescaled_size = copy.copy(self.size)
            if self.scene.matrix[1, 1] - self.scene.matrix[0, 0] / self.sides_ratio >= 0:
                self.rescaled_size *= self.scene.matrix[0, 0]
            else:
                self.rescaled_size *= self.scene.matrix[1, 1]

            self.rescaled_image = pygame.transform.scale(self.image, self.to_ints((self.size * self.pd_).tolist()))

        self.scene.s.blit(self.rescaled_image, self.scene.matrix @ self.center)

    @staticmethod
    def to_ints(iterable):
        for i in range(len(iterable)):
            iterable[i] = int(iterable[i])

        return iterable
