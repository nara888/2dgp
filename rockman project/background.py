import random

from pico2d import *

class Background:
    def __init__(self):
        self.image = load_image('stage.png')

    def draw(self):
        self.image.draw(400, 350, 800, 700)

