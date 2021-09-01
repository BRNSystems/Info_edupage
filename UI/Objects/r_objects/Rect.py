import pygame.draw


class Rect:
    def __init__(self, pos, size, color, scene):
        self.pos = pos
        self.size = size
        self.color = color
        self.rect = pygame.Rect(self.pos, self.size)
        self.scene = scene

    def blit(self):
        pygame.draw.rect(self.scene.s_, self.color, self.rect)
