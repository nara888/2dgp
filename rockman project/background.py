import random

from pico2d import *

class Background:
    def __init__(self):
        self.image = load_image('resource/stage/stage.png')
        self.bgm = load_wav('resource/bgm/JetManStage.wav')
        self.bgm.set_volume(64)
        self.bgm.repeat_play()

    def draw(self):
        self.image.draw(400, 350, 800, 700)

