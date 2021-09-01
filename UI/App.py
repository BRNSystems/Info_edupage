from multiprocessing import Queue
from multiprocessing import Process
import pygame
from pygame.locals import *
import sys


class App:
    def __init__(self, scene, edu, hands_ai):
        self.scene = scene
        self.edu = edu
        self.hands_ai = hands_ai

    def run(self):
        q = Queue()

        hands_ai_process = Process(target=self.hands_ai.run, args=(q,))

        while True:
            self.scene.redraw()

            for event in pygame.event.get():
                if event.type == QUIT:
                    hands_ai_process.terminate()
                    pygame.quit()
                    sys.exit(0)
