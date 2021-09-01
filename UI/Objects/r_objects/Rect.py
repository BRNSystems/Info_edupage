import pygame.draw
from numpy import array as a
import numpy as np


class Rect:
    def __init__(self, pos, size, color, scene):
        self.pos = pos
        self.size = size
        self.color = color
        self.rect = pygame.Rect(self.pos, self.size)
        self.scene = scene

    def blit(self):
        pygame.draw.rect(self.scene.s_, self.color, self.rect)
