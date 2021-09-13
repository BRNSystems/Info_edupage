import pygame.mouse

from numpy import array as a
import time

from GUI.Sample_Scenes.BasicScene import BasicScene

screen_size = a([200, 500])
scene = BasicScene(screen_size)

mouse_pos = [0, 0]
clicked = False

for i in range(400):
    scene.resize_screen(screen_size)
    scene.update()
    scene.update_mouse_events(pygame.mouse.get_pos(), pygame.mouse.get_pressed(3)[0])
    scene.progress()

    if i < 150:
        screen_size[0] += 3
    elif i < 250:
        screen_size[1] += 2
    else:
        pass
        screen_size -= 4

    time.sleep(0.1)
