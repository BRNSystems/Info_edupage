from UI.Scenes.VideoScene import VideoScene

from numpy import array as a
import time


screen_size = a([1200, 800])
scene = VideoScene(screen_size)

mouse_pos = [0, 0]
clicked = False

scene.update()
try:
    time.sleep(20)
except KeyboardInterrupt:
    pass

scene.stop_bgt_objects()
