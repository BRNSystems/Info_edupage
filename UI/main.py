from Scenes.BasicScene import BasicScene
from numpy import array as a
import time


scene = BasicScene(10, [600, 400])


while True:
    scene.redraw()
    time.sleep(0.1)
