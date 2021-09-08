import copy
import pygame
import time
import numpy as np
from numpy import array as a
from threading import Thread


class RefreshingImage:

    object_type = "nr_bgt"

    def __init__(self, center, scalar, path, scene, rps=24):
        self.center = center
        self.scalar = scalar
        self.path = path
        self.rps = rps  # refreshes per second
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

        self.updater = None
        self.updater_alive = True

        self.start_bg_activity()

    def start_bg_activity(self):
        self.updater_alive = True

        def update(self_):
            dt = 1 / self_.rps

            while self_.updater_alive:
                if self_.pd_ == self_.scene.pd_:
                    try:
                        self_.image = pygame.image.load(self_.path).convert()
                    except:
                        pass
                    else:
                        self_.image = pygame.transform.scale(self_.image,
                                                             self_.to_ints((a(self_.image.get_size())
                                                                            * self_.scalar).tolist()))
                        self_.rescaled_image = pygame.transform.scale(self_.image,
                                                                      self_.to_ints((self_.size * self_.pd_).tolist()))
                        self_.scene.s.blit(self_.rescaled_image, self_.scene.matrix @ self_.center)
                        pygame.display.update()

                time.sleep(dt)

        self.updater = Thread(target=update, args=(self,))
        self.updater.start()

    def stop_bg_activity(self):
        self.updater_alive = False

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
