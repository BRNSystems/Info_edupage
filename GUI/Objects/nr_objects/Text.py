import pygame


class Text:

    object_type = "nr"

    def __init__(self, position, text, font_size, color, scene, font_name="calibri", bold=True):
        self.position = position
        self.text = text
        self.font_size = font_size
        self.font_name = font_name
        self.bold = bold
        self.color = color
        self.scene = scene
        self.scalar = self.scene.matrix[0, 0]

        self.font = pygame.font.SysFont(self.font_name, max(1, int(self.font_size * self.scalar)), self.bold)
        self.rendered_text = self.font.render(self.text, False, self.color)

        self.blit_position = self.scene.matrix @ self.position
        self.blit_position[0] -= self.rendered_text.get_width() / 2
        self.blit_position[1] -= self.rendered_text.get_height() / 2

    def blit(self):
        if self.scalar != self.scene.matrix[0, 0]:
            self.scalar = self.scene.matrix[0, 0]
            self.font = pygame.font.SysFont(self.font_name, max(1, int(self.font_size * self.scalar)), self.bold)
            self.rendered_text = self.font.render(self.text, False, self.color)

            self.blit_position = self.scene.matrix @ self.position
            self.blit_position[0] -= self.rendered_text.get_width() / 2
            self.blit_position[1] -= self.rendered_text.get_height() / 2

        self.scene.s.blit(self.rendered_text, self.blit_position)
