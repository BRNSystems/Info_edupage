from numpy import array as a
import pygame
import math


class EquilateralTriangle:
    def __init__(self, position, side_length, rotation, color, scene, width=0):
        self.position = position
        self.side_length = side_length
        self.rotation = rotation
        self.color = color
        self.scene = scene
        self.width = width
        self.rotation_point = complex(math.cos(rotation), math.sin(rotation))

        self.pd_ = self.scene.pd_

        self.points = a([
            complex(0, self.side_length),
            complex(self.side_length, self.side_length),
            complex(self.side_length * 0.5,
                    self.side_length - math.sqrt(self.side_length ** 2 - (self.side_length * 0.5) ** 2))
        ])
        self.points -= complex(self.side_length * 0.5, self.side_length * 0.5)
        self.points *= self.rotation_point * self.pd_
        self.points += complex(self.side_length * 0.5, self.side_length * 0.5)
        rescaled_position = self.scene.matrix @ self.position
        self.points += complex(rescaled_position[0], rescaled_position[1])
        self.points = [[point.real, point.imag] for point in self.points]

    def blit(self):
        if self.pd_ != self.scene.pd_:
            self.pd_ = self.scene.pd_

            self.points = a([
                complex(0, self.side_length),
                complex(self.side_length, self.side_length),
                complex(self.side_length * 0.5,
                        self.side_length - math.sqrt(self.side_length ** 2 - (self.side_length * 0.5) ** 2))
            ])
            self.points -= complex(self.side_length * 0.5, self.side_length * 0.5)
            self.points *= self.rotation_point * self.pd_
            self.points += complex(self.side_length * 0.5, self.side_length * 0.5)
            rescaled_position = self.scene.matrix @ self.position
            self.points += complex(rescaled_position[0], rescaled_position[1])
            self.points = [[point.real, point.imag] for point in self.points]

        pygame.draw.polygon(self.scene.s, self.color, self.points, self.width)

