import pygame.draw


class Circle:
    def __init__(self, center, radius, color, scene):
        self.center = center
        self.radius = radius
        self.color = color
        self.scene = scene

    def blit(self):
        pygame.draw.circle(self.scene.s, self.color,
                           self.scene.matrix @ self.center,
                           self.radius * self.scene.pd_)
