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

    HORIZON_BB_WIDTH = HORIZON_X_SIZE / 2
    HORIZON_BB_HEIGHT = HORIZON_Y_SIZE / 2

    # 45도 미사일
    OPPOSITE_MISSILE = 1
    OPPOSITE_MISSILE_X_SIZE = 25
    OPPOSITE_MISSILE_Y_SIZE = 25

    OPPOSITE_X_SIZE = OPPOSITE_MISSILE_X_SIZE * 3
    OPPOSITE_Y_SIZE = OPPOSITE_MISSILE_Y_SIZE * 3

    OPPOSITE_BB_WIDTH = 30
    OPPOSITE_BB_HEIGHT = 30

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

    def get_bb(self):
        if self.type == self.HORIZON_MISSILE:
            return self.x - self.HORIZON_BB_WIDTH, self.y - self.HORIZON_BB_HEIGHT, self.x + self.HORIZON_BB_WIDTH, self.y + self.HORIZON_BB_HEIGHT
        elif self.type == self.OPPOSITE_MISSILE:
            return self.x - self.OPPOSITE_BB_WIDTH, self.y - self.OPPOSITE_BB_HEIGHT, self.x + self.OPPOSITE_BB_WIDTH, self.y + self.OPPOSITE_BB_HEIGHT


    def draw_bb(self):
        draw_rectangle(*self.get_bb())

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


class JetMan_Bomb(Boss_Bullet):

    PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
    BOMB_SPEED_KMPH = 15.0  # Km / Hour
    BOMB_SPEED_MPM = (BOMB_SPEED_KMPH * 1000.0 / 60.0)
    BOMB_SPEED_MPS = (BOMB_SPEED_MPM / 60.0)
    BOMB_SPEED_PPS = (BOMB_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    image = None

    # 이미지 사이즈
    BOMB_IMAGE_X_SIZE = 10
    BOMB_IMAGE_Y_SIZE = 20

    BOMB_X_SIZE = BOMB_IMAGE_X_SIZE * 3
    BOMB_Y_SIZE = BOMB_IMAGE_Y_SIZE * 3

    BB_WIDTH = BOMB_X_SIZE / 2
    BB_HEIGHT = BOMB_Y_SIZE / 2


    def __init__(self, jetman):
        if self.image == None:
            self.image = load_image('resource/boss/jetman/jetman_bomb.png')

        self.dir = jetman.dir
        self.x = jetman.x
        self.y = jetman.y - 50
        self.action_start_time = get_time()  # 낙하 시작 시간
        self.accel = 1200  # 초기 낙하 가속

    ##
    def move(self, frame_time):
        x_distance = self.BOMB_SPEED_PPS * frame_time * self.dir
        self.x += x_distance

        gap_time = 0.1
        if get_time() - self.action_start_time < gap_time * 1:
            y_distance = self.accel * frame_time / 6
        elif get_time() - self.action_start_time >= gap_time * 1 and get_time() - self.action_start_time < gap_time * 2:
            y_distance = self.accel * frame_time / 4
        elif get_time() - self.action_start_time >= gap_time * 2 and get_time() - self.action_start_time < gap_time * 3:
            y_distance = self.accel * frame_time / 3
        elif get_time() - self.action_start_time >= gap_time * 3 and get_time() - self.action_start_time < gap_time * 4:
            y_distance = self.accel * frame_time / 2
        elif get_time() - self.action_start_time >= gap_time * 4 and get_time() - self.action_start_time < gap_time * 5:
            y_distance = self.accel * frame_time / 1.5
        elif get_time() - self.action_start_time >= gap_time * 5:
            y_distance = self.accel * frame_time

        self.y -= y_distance


    def update(self, frame_time):
        self.move(frame_time)

    def get_bb(self):
        return self.x - self.BB_WIDTH, self.y - self.BB_HEIGHT, self.x + self.BB_WIDTH, self.y + self.BB_HEIGHT

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def draw(self):
        self.image.clip_draw(0, 0, self.BOMB_IMAGE_X_SIZE, self.BOMB_IMAGE_Y_SIZE, self.x, self.y, self.BOMB_X_SIZE, self.BOMB_Y_SIZE)
