import pygame.mouse

from UI.Scenes.BasicScene import BasicScene
from UI.Scenes.BasicMultiscene import BasicMultiscene
from UI.Scenes.MultisceneInMultiscene import MultisceneInMultiscene
from UI.Scenes.RopeScene import RopeScene
from UI.Scenes.RopeMultiscene import RopeMultiscene
from UI.Scenes.VideoScene import VideoScene

from numpy import array as a
import time

screen_size = a([200, 500])
scene = VideoScene(screen_size)

mouse_pos = [0, 0]
clicked = False


for i in range(400):
    scene.resize_screen(screen_size)
    scene.update()
    scene.update_mouse_events(pygame.mouse.get_pos(), pygame.mouse.get_pressed(3)[0])
    scene.progress()
    #scene.save(f"Render/{i}.png", [800, 800])

    if i < 150:
        screen_size[0] += 3
    elif i < 250:
        screen_size[1] += 2
    else:
        pass
        screen_size -= 4

    time.sleep(0.01)

scene.stop_bgt_objects()
