from numpy import array
import pygame
import math


class Rope:

    object_type = "nr_d_i"

    class Node:
        def __init__(self, position):
            self.position = position
            self.previous_position = position
            self.locked = False

        def progress(self, gravity):
            if self.locked is False:
                position_before_update = self.position
                self.position += self.position - self.previous_position
                self.position[1] += gravity
                self.previous_position = position_before_update

    class Connection:
        def __init__(self, a, b, length):
            self.a = a
            self.b = b
            self.length = length

        def balance(self):
            center = (self.a.position + self.b.position) * 0.5
            connection_vector = (self.b.position - self.a.position)
            connection_vector /= math.sqrt(sum(connection_vector ** 2))
            connection_vector *= self.length * 0.5

            if self.b.locked is False:
                self.b.position = center + connection_vector
            if self.a.locked is False:
                self.a.position = center - connection_vector

    def __init__(self, position, length, nodes_n, nodes_r, rope_width, scene, gravity=2, start_angle=1,
                 balance_amount=10, node_color=(255, 100, 100), rope_color=(255, 160, 160)):
        self.position = position
        self.length = length
        self.nodes_n = nodes_n
        self.nodes_r = nodes_r
        self.rope_width = rope_width
        self.gravity = gravity
        self.start_angle = start_angle
        self.balance_amount = balance_amount
        self.scene = scene
        self.node_color = node_color
        self.rope_color = rope_color
        self.pd_ = self.scene.pd_

        self.initial_direction = array([math.cos(self.start_angle), math.sin(self.start_angle)])

        self.rope_segment_length = self.length / (self.nodes_n - 1)
        self.rescaled_rope_segment_length = self.rope_segment_length * self.pd_
        self.rescaled_nodes_r = self.nodes_r * self.pd_
        self.rescaled_rope_width = self.rope_width * self.scene.pd_

        self.nodes = [self.Node(self.position +
                                self.initial_direction * i * self.rescaled_rope_segment_length)
                      for i in range(self.nodes_n)]

        self.nodes[0].locked = True

        self.connections = [self.Connection(self.nodes[i], self.nodes[i + 1], self.rescaled_rope_segment_length)
                            for i in range(len(self.nodes) - 1)]

    def progress(self):
        for node in self.nodes:
            node.progress(self.gravity)

        for _ in range(self.balance_amount):
            for connection in self.connections:
                connection.balance()

    def blit(self):
        if self.pd_ != self.scene.pd_:
            self.pd_ = self.scene.pd_

            self.rescaled_rope_segment_length = self.rope_segment_length * self.pd_
            self.rescaled_nodes_r = self.nodes_r * self.pd_
            self.rescaled_rope_width = self.rope_width * self.pd_

            for connection in self.connections:
                connection.length = self.rescaled_rope_segment_length

        for i in range(len(self.nodes) - 1):
            pygame.draw.line(self.scene.s, self.rope_color,
                             self.scene.matrix @ self.nodes[i].position,
                             self.scene.matrix @ self.nodes[i + 1].position,
                             max(1, int(self.rescaled_rope_width)))

        for node in self.nodes:
            pygame.draw.circle(self.scene.s, self.node_color, self.scene.matrix @ node.position,
                               max(1, self.rescaled_nodes_r))

    @staticmethod
    def to_ints(iterable):
        for i in range(len(iterable)):
            iterable[i] = int(iterable[i])

        return iterable
