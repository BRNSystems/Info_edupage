from numpy import array as a
import numpy as np
import pygame


class Screen:
    def __init__(self, width: float, height: float, font_size: int, matrix: np.array):
        self.width = width
        self.height = height
        self.size = a([width, height])
        self.matrix = matrix

        self.s = pygame.Surface([width, height])

        self.font_size = font_size

        self.center = a([width, height]) / 2
