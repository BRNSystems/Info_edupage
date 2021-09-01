import pygame.draw


class Line:
    def __init__(self, a, b, width, color, scene):
        self.a = a
        self.b = b
        self.width = width
        self.color = color
        self.scene = scene

    def blit(self):
        pygame.draw.line(self.scene.s, self.color, self.scene.matrix @ self.a, self.scene.matrix @ self.b,
                         int(self.width * self.scene.pd))
