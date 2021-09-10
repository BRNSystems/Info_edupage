from numpy import array as a
import time
from UI.Scenes.LuminousCircleEffectScene import LuminousCircleEffectScene


screen_size = a([1000, 800])
scene = LuminousCircleEffectScene(screen_size)


scene.update()
for i in range(400):

    scene.update()
    scene.save(f"Render/{i}.png", screen_size)

    time.sleep(0.05)

