from UI.Objects.Scene import Scene
from numpy import array as a

from UI.Objects.nr_objects.background_threaded_objects.RefreshingImage import RefreshingImage


class VideoScene(Scene):
    def __init__(self, screen_size, bg=(60, 60, 60)):

        s__size = [1200, 800]

        super().__init__(*s__size, screen_size, bg)

        ri0 = RefreshingImage(a([100, 100]), 1.2, "video_capture.png", self)

        self.sort_objects(ri0)
