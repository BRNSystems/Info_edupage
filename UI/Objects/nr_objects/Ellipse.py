import pygame


class Ellipse:
    def __init__(self, center, a, b, color, scene):
        self.center = center
        self.a = a
        self.b = b
        self.color = color
        self.scene = scene

    def blit(self):
        a_ = self.a * self.scene.pd_
        b_ = self.b * self.scene.pd_
        center_ = self.scene.matrix @ self.center
        center_ = [center_[0] - a_, center_[1] - b_]

        pygame.draw.ellipse(self.scene.s, self.color,
                            pygame.Rect(center_, [a_ * 2, b_ * 2]))
