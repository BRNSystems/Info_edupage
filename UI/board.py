import pygame.draw
from rounded_rect import draw_rounded_rect


class Board:
    def __init__(self, size, bg_image):
        self.fs = False
        self.dp = [0, 0]
        self.bg_image = bg_image
        self.size = size
        self.width = size[0]
        self.height = size[1]

        self.width_fifth = self.width / 5
        self.small_size_fraction = sum(self.size) / 60
        self.mid_width = self.width - self.width_fifth - 2 * self.small_size_fraction

        self.height_sixth = self.height / 6

        self.transparent_objects_color = (237, 237, 250)

    def draw_bg(self, display):
        # drawing left rect
        pygame.draw.rect(display, (49, 49, 54), pygame.Rect(0, 0, self.width_fifth, self.height))

        # drawing bg image
        display.blit(self.bg_image, [self.width_fifth, 0])

        # drawing top and bottom rect
        surf = pygame.Surface(self.size)
        surf.fill((0, 0, 0))
        draw_rounded_rect(surf, pygame.Rect(self.width_fifth + self.small_size_fraction,
                                            self.small_size_fraction, self.mid_width,
                                            100),
                          self.transparent_objects_color, int(self.height / 20))
        pygame.draw.rect(surf, self.transparent_objects_color, pygame.Rect(self.width_fifth, self.height - self.height_sixth,
                                                                           self.width, self.height_sixth))
        surf.set_colorkey((0, 0, 0))
        surf.set_alpha(100)
        display.blit(surf, [0, 0])
