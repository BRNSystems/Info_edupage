from numpy import array as a
import time

from UI.Scenes.Sample_Scenes.LuminousCircleEffectMultiscene import LuminousCircleEffectMultiscene
from UI.Scenes.Sample_Scenes.LuminousCircleEffectScene import LuminousCircleEffectScene


screen_size = a([1000, 800])
scene = LuminousCircleEffectMultiscene(screen_size)


scene.update()
for i in range(400):

    scene.light_update()

    time.sleep(0.05)

