import pygame
from pygame.locals import *
import math
import numpy as np
import random
import time
import json
import os
import sys
import copy
from board import Board


# basic config
pygame.mixer.pre_init(48000, -16, 2, 512)
pygame.init()
pygame.mixer.set_num_channels(16)
available = pygame.font.get_fonts()
monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]

font = pygame.font.SysFont('calibri', 60, True)
small_font = pygame.font.SysFont('calibri', 40, True)
tiny_font = pygame.font.SysFont('calibri', 20, True)

Window_size = [1200, 800]
Default_size = Window_size
screen = pygame.display.set_mode(Window_size)
display = pygame.Surface(Window_size)
pygame.display.set_caption("School_board")
pygame.display.set_icon(pygame.image.load("logo.png").convert())
clock = pygame.time.Clock()
Win_size = Window_size


alive = True
board = Board(Window_size, pygame.image.load("board_bg.png"))

while alive:

    board.draw_bg(display)

    # event loop

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit(0)

        # keydown
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit(0)
            elif event.key == K_f:
                board.fs = not board.fs
                if board.fs is False:
                    Win_size = Default_size
                    screen = pygame.display.set_mode(Win_size)
                    board.dp = [0, 0]
                else:
                    screen = pygame.display.set_mode(monitor_size, pygame.FULLSCREEN)
                    d = screen
                    ratio = [Default_size[1] / Default_size[0], Default_size[0] / Default_size[1]]
                    # u chose width or height here

                    if Default_size[0] > Default_size[1]:
                        Win_size = [d.get_width(), int(d.get_width() * ratio[0])]
                        d = d.get_height()
                        dd = Win_size[1]
                    else:
                        Win_size = [int(d.get_height() * ratio[1]), d.get_height()]
                        d = pygame.display.get_surface().get_width()
                        dd = Win_size[0]
                        board.dp[0] = (d - dd) / 2

                    screen = screen

    # basic loop config

    screen.blit(pygame.transform.scale(display, Win_size), board.dp)
    pygame.display.update()
    clock.tick(10)
