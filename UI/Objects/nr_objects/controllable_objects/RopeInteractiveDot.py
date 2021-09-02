import math
import pygame


class RopeInteractiveDot:
    def __init__(self, position, r, color, force, forcefield_range, scene):
        self.position = position
        self.r = r
        self.color = color
        self.force = force
        self.forcefield_range = forcefield_range
        self.scene = scene

    def blit(self):
        pygame.draw.circle(self.scene.s, self.color, self.scene.matrix @ self.position, self.r)

    def input(self, mouse_pos, clicked):
        self.position = mouse_pos

        if clicked:
            for object_ in self.scene.nrd_objects:
                if object_.__class__.__name__ == "Rope":
                    for node in object_.nodes:
                        if math.sqrt(sum((node.position - self.position) ** 2)) < self.forcefield_range:
                            force_vector = node.position - self.position
                            force_vector /= math.sqrt(sum(force_vector ** 2))
                            force_vector *= self.force

                            node.position += force_vector


