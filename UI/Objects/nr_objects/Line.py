import pygame.draw


class Line:

    object_type = "nr"

    def __init__(self, a, b, width, color, scene):
        self.a = a
        self.b = b
        self.width = width
        self.color = color
        self.scene = scene

    def blit(self):
        pygame.draw.line(self.scene.s, self.color, self.scene.matrix @ self.a, self.scene.matrix @ self.b,
                         max(1, int(self.width * self.scene.pd)))
