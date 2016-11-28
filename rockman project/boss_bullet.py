from pico2d import *
import math


class Boss_Bullet:
    image = None

    PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
    BULLET_SPEED_KMPH = 60.0  # Km / Hour
    BULLET_SPEED_MPM = (BULLET_SPEED_KMPH * 1000.0 / 60.0)
    BULLET_SPEED_MPS = (BULLET_SPEED_MPM / 60.0)
    BULLET_SPEED_PPS = (BULLET_SPEED_MPS * PIXEL_PER_METER)

    BULLET_SIZE = 30

    def __init__(self, player):
        pass


    def move(self, frame_time):
        pass

    def update(self, frame_time):
        self.move(frame_time)

    def draw(self):
        pass

class JetMan_Missile(Boss_Bullet):

    PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
    MISSILE_SPEED_KMPH = 160.0  # Km / Hour
    MISSILE_SPEED_MPM = (MISSILE_SPEED_KMPH * 1000.0 / 60.0)
    MISSILE_SPEED_MPS = (MISSILE_SPEED_MPM / 60.0)
    MISSILE_SPEED_PPS = (MISSILE_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    image_H = None
    image_O = None

    # 수평 미사일
    HORIZON_MISSILE = 0
    HORIZON_MISSILE_X_SIZE = 32
    HORIZON_MISSILE_Y_SIZE = 10

    HORIZON_X_SIZE = HORIZON_MISSILE_X_SIZE * 3
    HORIZON_Y_SIZE = HORIZON_MISSILE_Y_SIZE * 3

    # 45도 미사일
    OPPOSITE_MISSILE = 1
    OPPOSITE_MISSILE_X_SIZE = 25
    OPPOSITE_MISSILE_Y_SIZE = 25

    OPPOSITE_X_SIZE = OPPOSITE_MISSILE_X_SIZE * 3
    OPPOSITE_Y_SIZE = OPPOSITE_MISSILE_Y_SIZE * 3

    def __init__(self, jetman, player):
        if JetMan_Missile.image_H == None:
            JetMan_Missile.image_H = load_image('resource/boss/jetman/jetman_missile2.png')
        if JetMan_Missile.image_O == None:
            JetMan_Missile.image_O = load_image('resource/boss/jetman/jetman_missile1.png')

        if jetman.y < 500:
            self.type = self.HORIZON_MISSILE
        else:
            self.type = self.OPPOSITE_MISSILE

        self.dir = jetman.dir
        self.x = jetman.x
        self.y = jetman.y
        self.target_x = player.x
        self.target_y = player.y
        self.frame = 0
        self.total_frames = 0.0

        fVx = self.x - self.target_x
        fVy = self.y - self.target_y
        fLength = math.sqrt((fVx*fVx)+(fVy*fVy))
        self.fDirX = fVx / fLength  # 단위벡터
        self.fDirY = fVy / fLength


    def move(self, frame_time):
        x_distance = self.fDirX * self.MISSILE_SPEED_PPS * frame_time
        y_distance = self.fDirY * self.MISSILE_SPEED_PPS * frame_time
        self.x -= x_distance
        self.y -= y_distance


    def update(self, frame_time):
        self.total_frames += self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 2
        self.move(frame_time)

    def draw(self):
        if self.type == self.HORIZON_MISSILE:
            if self.dir == 1:
                self.image_H.clip_draw(self.HORIZON_MISSILE_X_SIZE * self.frame, self.HORIZON_MISSILE_Y_SIZE * 1, self.HORIZON_MISSILE_X_SIZE,
                                     self.HORIZON_MISSILE_Y_SIZE,
                                     self.x, self.y, self.HORIZON_X_SIZE, self.HORIZON_Y_SIZE)
            elif self.dir == -1:
                self.image_H.clip_draw(self.HORIZON_MISSILE_X_SIZE * self.frame, self.HORIZON_MISSILE_Y_SIZE * 0, self.HORIZON_MISSILE_X_SIZE,
                                     self.HORIZON_MISSILE_Y_SIZE,
                                     self.x, self.y, self.HORIZON_X_SIZE, self.HORIZON_Y_SIZE)
        elif self.type == self.OPPOSITE_MISSILE:
            if self.dir == 1:
                self.image_O.clip_draw(self.OPPOSITE_MISSILE_X_SIZE * self.frame, self.OPPOSITE_MISSILE_Y_SIZE * 1, self.OPPOSITE_MISSILE_X_SIZE,
                                     self.OPPOSITE_MISSILE_Y_SIZE,
                                     self.x, self.y, self.OPPOSITE_X_SIZE, self.OPPOSITE_Y_SIZE)
            elif self.dir == -1:
                self.image_O.clip_draw(self.OPPOSITE_MISSILE_X_SIZE * self.frame, self.OPPOSITE_MISSILE_Y_SIZE * 0, self.OPPOSITE_MISSILE_X_SIZE,
                                     self.OPPOSITE_MISSILE_Y_SIZE,
                                     self.x, self.y, self.OPPOSITE_X_SIZE, self.OPPOSITE_Y_SIZE)