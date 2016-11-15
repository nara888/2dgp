import sys
sys.path.append('../LabsAll/Labs')

from pico2d import *

# Enemy 추상 클래스
# 상속받아 각각의 적들을 만든다
class Enemy:

    image = None
    def __init__(self):
        pass

    # 이동
    def move(self, frame_time):
        pass

    # 슬라이딩
    def sliding(self, frame_time):
        pass

    # 점프
    def jump(self, frame_time):
        pass


    # 낙하
    def fall(self, frame_time):
        pass

    # 발사
    def shot(self, frame_time):
        pass

    # 사망
    def dead(self, frame_time):
        pass



    def get_bb(self):
        pass

    def draw_bb(self):
        pass


    def handle_event(self, event):
        pass


    def update(self, frame_time):
        pass

    def draw(self):
        pass



class Mr_shiniri(Enemy):

    PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
    RUN_SPEED_KMPH = 40.0  # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    X_SIZE = 150
    Y_SIZE = 150
    SPRITE_ANIMATION_NUM = 2
    image = None

    def __init__(self):
        if Mr_shiniri.image == None:
            Mr_shiniri.image = load_image('resource/enemy/Mrshiniri_100x50.png')

        self.x, self.y = 800, 150
        self.dir = -1
        self.frame = 0
        self.total_frames = 0

    # 이동
    def move(self, frame_time):
        distance = self.RUN_SPEED_PPS * frame_time
        self.x += (self.dir * distance)

    # 슬라이딩
    def sliding(self, frame_time):
        pass

    # 점프
    def jump(self, frame_time):
        pass

    # 낙하
    def fall(self, frame_time):
        pass

    # 발사
    def shot(self, frame_time):
        pass

    # 사망
    def dead(self, frame_time):
        pass

    def get_bb(self):
        pass

    def draw_bb(self):
        pass

    def handle_event(self, event):
        pass

    def update(self, frame_time):
        self.total_frames += self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % self.SPRITE_ANIMATION_NUM

        self.move(frame_time)

    def draw(self):
        self.image.clip_draw(self.frame * 50, 0, 50, 50, self.x, self.y, self.X_SIZE, self.Y_SIZE)
