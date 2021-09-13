import math
import random
import numpy as np
from numpy import array
from pygame.draw import circle


class LuminousCircleEffect:

    object_type = "nr_l"

    def __init__(self, position, r, color, scene, circles_n=20, point_speed=0.02, movement_stability=5):
        self.position = position
        self.r = r
        self.color = color
        self.scene = scene
        self.circles_n = circles_n
        self.point_speed = point_speed
        self.point_speed_inverse = 1 / self.point_speed
        self.movement_stability = movement_stability

        self.point_position = array([0., 0.])
        self.point_velocity = array([0., 0.])

    def update(self):
        self.point_position += self.point_velocity

        a = math.sqrt(sum(self.point_position ** 2))

        if a > 1:
            self.point_position /= a
            a = 1

        b = 1 - a
        c = (0.5 * a) + b
        d = math.sqrt((c ** 2) - ((a * 0.5) ** 2))

        if a == 0:
            rotation_point = complex(1, 0)
        else:
            normalized_point_position = self.point_position / a
            rotation_point = complex(*normalized_point_position)

        delta = random.uniform(0, math.tau)
        m = max(random.uniform(0, 1), random.uniform(0, 1))

        point_position = complex(math.cos(delta) * m * c, math.sin(delta) * m * d) * rotation_point
        point_position = array([point_position.real, point_position.imag])

        self.point_velocity *= self.movement_stability * self.point_speed_inverse
        self.point_velocity += point_position - self.point_position
        self.point_velocity /= math.sqrt(sum(self.point_velocity ** 2))
        self.point_velocity *= self.point_speed

    def blit(self, light_blit=False):
        if light_blit:
            s, transformed_position = self.scene.get_info_for_light_objects(self.position)

            rescaled_r = self.r * self.scene.pd_

            x = np.linspace(0, self.point_position[0], self.circles_n) * rescaled_r
            y = np.linspace(0, self.point_position[1], self.circles_n) * rescaled_r
            r = np.linspace(rescaled_r, 0, self.circles_n)

            c = [np.linspace(value, 255, self.circles_n) for value in self.color]

            for i in range(self.circles_n - 1):
                circle(s, (c[0][i], c[1][i], c[2][i]),
                       transformed_position + array([x[i], y[i]]), r[i])
        else:
            rescaled_r = self.r * self.scene.pd_
            transformed_position = self.scene.matrix @ self.position

            x = np.linspace(0, self.point_position[0], self.circles_n) * rescaled_r
            y = np.linspace(0, self.point_position[1], self.circles_n) * rescaled_r
            r = np.linspace(rescaled_r, 0, self.circles_n)

            c = [np.linspace(value, 255, self.circles_n) for value in self.color]

            for i in range(self.circles_n - 1):
                circle(self.scene.s, (c[0][i], c[1][i], c[2][i]),
                       transformed_position + array([x[i], y[i]]), r[i])
