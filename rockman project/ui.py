from pico2d import *
from boss import *

class Bar:
    bar_image = None
    tic_image = None

    BAR_IMAGE_WIDTH = 8     # 바 원본이미지 크기
    BAR_IMAGE_HEIGHT = 56
    TIC_IMAGE_WIDTH = 6     # 틱 원본이미지 크기
    TIC_IMAGE_HEIGHT = 2

    BAR_WIDTH = BAR_IMAGE_WIDTH * 3     # 바 크기
    BAR_HEIGHT = BAR_IMAGE_HEIGHT * 3
    TIC_WIDTH = TIC_IMAGE_WIDTH * 3     # 틱 크기
    TIC_HEIGHT = TIC_IMAGE_HEIGHT * 3

    def __init__(self):
        self.x, self.y = 50, 550
        if self.bar_image == None:
            self.bar_image = load_image('resource/ui/hp_bar.png')
        if self.tic_image == None:
            self.tic_image = load_image('resource/ui/hp_tic.png')

    def update(self, frame_time):
        pass

    def draw(self):
        self.bar_image.draw(self.x, self.y, self.BAR_WIDTH, self.BAR_HEIGHT)
        for i in range(0,28):
            self.tic_image.draw(self.x, self.y - self.BAR_HEIGHT // 2 + 3 + (6*i), self.TIC_WIDTH, self.TIC_HEIGHT)

class Hp_Bar(Bar):
    bar_image = None
    tic_image = None

    BAR_IMAGE_WIDTH = 8     # 바 원본이미지 크기
    BAR_IMAGE_HEIGHT = 56
    TIC_IMAGE_WIDTH = 6     # 틱 원본이미지 크기
    TIC_IMAGE_HEIGHT = 2

    BAR_WIDTH = BAR_IMAGE_WIDTH * 3     # 바 크기
    BAR_HEIGHT = BAR_IMAGE_HEIGHT * 3
    TIC_WIDTH = TIC_IMAGE_WIDTH * 3     # 틱 크기
    TIC_HEIGHT = TIC_IMAGE_HEIGHT * 3

    def __init__(self, player):
        self.x, self.y = 50, 550
        self.player = player
        if self.bar_image == None:
            self.bar_image = load_image('resource/ui/hp_bar.png')
        if self.tic_image == None:
            self.tic_image = load_image('resource/ui/hp_tic.png')

    def update(self, frame_time):
        pass

    def draw(self):
        self.bar_image.draw(self.x, self.y, self.BAR_WIDTH, self.BAR_HEIGHT)
        for i in range(0,self.player.hp):
            self.tic_image.draw(self.x, self.y - self.BAR_HEIGHT // 2 + 3 + (6*i), self.TIC_WIDTH, self.TIC_HEIGHT)

class Boss_Hp_Bar(Bar):
    bar_image = None
    tic_image = None

    BAR_IMAGE_WIDTH = 8     # 바 원본이미지 크기
    BAR_IMAGE_HEIGHT = 56
    TIC_IMAGE_WIDTH = 6     # 틱 원본이미지 크기
    TIC_IMAGE_HEIGHT = 2

    BAR_WIDTH = BAR_IMAGE_WIDTH * 3     # 바 크기
    BAR_HEIGHT = BAR_IMAGE_HEIGHT * 3
    TIC_WIDTH = TIC_IMAGE_WIDTH * 3     # 틱 크기
    TIC_HEIGHT = TIC_IMAGE_HEIGHT * 3

    def __init__(self, boss):
        self.x, self.y = 100, 550
        self.boss = boss
        if self.bar_image == None:
            self.bar_image = load_image('resource/ui/hp_bar.png')
        if self.tic_image == None:
            if type(self.boss) == JetMan:
                self.tic_image = load_image('resource/ui/jetman_tic.png')

    def update(self, frame_time):
        pass

    def draw(self):
        self.bar_image.draw(self.x, self.y, self.BAR_WIDTH, self.BAR_HEIGHT)
        for i in range(0,self.boss.hp):
            self.tic_image.draw(self.x, self.y - self.BAR_HEIGHT // 2 + 3 + (6*i), self.TIC_WIDTH, self.TIC_HEIGHT)