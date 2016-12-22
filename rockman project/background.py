from pico2d import *

class Background:

    image = None
    bgm = None

    def __init__(self):
        if self.image == None:
            self.image = load_image('resource/stage/stage.png')

    """
    def music_start(self):
        if self.bgm == None:
            self.bgm = load_music('resource/bgm/BossBattle.ogg')
            self.bgm.set_volume(64)
            self.bgm.repeat_play()
    """

    def draw(self):
        self.image.draw(400, 350, 800, 700)

