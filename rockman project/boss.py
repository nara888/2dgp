import sys
import random
sys.path.append('../LabsAll/Labs')

from pico2d import *
from boss_bullet import *
from player import *


# Enemy 추상 클래스
# 상속받아 각각의 적들을 만든다
class Boss:

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


class JetMan(Boss):

    PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
    FLYING_X_SPEED_KMPH = 60.0  # Km / Hour
    FLYING_X_SPEED_MPM = (FLYING_X_SPEED_KMPH * 1000.0 / 60.0)
    FLYING_X_SPEED_MPS = (FLYING_X_SPEED_MPM / 60.0)
    FLYING_X_SPEED_PPS = (FLYING_X_SPEED_MPS * PIXEL_PER_METER)

    FLYING_Y_SPEED_KMPH = 25.0  # Km / Hour
    FLYING_Y_SPEED_MPM = (FLYING_Y_SPEED_KMPH * 1000.0 / 60.0)
    FLYING_Y_SPEED_MPS = (FLYING_Y_SPEED_MPM / 60.0)
    FLYING_Y_SPEED_PPS = (FLYING_Y_SPEED_MPS * PIXEL_PER_METER)

    JUMP_POWER = 1300

    BOMBING_X_SPEED_PPS = FLYING_X_SPEED_PPS * 1.5
    LANDING_Y_SPEED_PPS = FLYING_Y_SPEED_PPS * 0.7

    TIME_PER_ACTION = 2
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    TIME_PER_ROCK = 0.8
    ROCK_PER_TIME = 1.0 / TIME_PER_ROCK

    IMAGE_SIZE = 60
    ROCK_IMAGE_SIZE = 35

    X_SIZE = 180
    Y_SIZE = X_SIZE

    ROCK_SIZE = 120

    LEFT_DIR = -1
    RIGHT_DIR = 1

    SPRITE_ANIMATION_NUM = 2
    ROCK_ANI_NUM = 3

    image = None
    rock_on_image = None

    GROUND_LINE = 150
    Y_LANDING_START = 400
    Y_FLYING_START = 600

    X_LEFT_TAKEOFF_START = 250
    X_RIGHT_TAKEOFF_START = 550

    X_LEFT_LANDING_STOP = 100
    X_RIGHT_LANDING_STOP = 700

    X_LEFT_FLYING_STOP = -100
    X_RIGHT_FLYING_STOP = 900

    RIGHT_STAND, LEFT_STAND, RIGHT_RUN, LEFT_RUN, RIGHT_FLYING, LEFT_FLYING, \
    RIGHT_LANDING, LEFT_LANDING, RIGHT_TAKE_OFF, LEFT_TAKE_OFF, \
    RIGHT_JUMP, LEFT_JUMP, RIGHT_FALL, LEFT_FALL, \
    RIGHT_BOMBING, LEFT_BOMBING, LEFT_MISSILE, RIGHT_MISSILE, READY \
        = 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18

    def __init__(self):
        if self.image == None:
            self.image = load_image('resource/boss/jetman/jetman_240x540.png')
        if self.rock_on_image == None:
            self.rock_on_image = load_image('resource/boss/jetman/jetman_rockon.png')

        self.x, self.y = -150, self.Y_LANDING_START
        self.dir = self.RIGHT_DIR
        self.frame = 0
        self.total_frames = 0
        self.state = self.RIGHT_LANDING  # 플레이어 상태
        self.shot_state = False  # 샷 상태
        self.shot_start_time = 0  # 샷 시작 시간
        self.trigger_enter = True   # 최초 등장
        self.trigger_ready = False # 전투 준비
        self.trigger_take_off = False # 이륙
        self.trigger_flying = False # 비행
        self.trigger_landing = False    # 착륙
        self.trigger_jump = False   # 점프
        self.trigger_bombing = False # 폭격
        self.trigger_missile = False # 미사일 공격
        self.ready_time = 0
        self.ready_start_time = 0
        self.ready_frame = 0
        self.jump_frame = 0

        self.rock_x = 0
        self.rock_y = 0
        self.rock_frame = 0
        self.rock_total_frames = 0
        self.rock_state = False

        self.jetman_missile = None
        self.jetman_bomb_list = []

    # 스테이지 등장
    def enter_stage(self, frame_time):
        distance = self.FLYING_X_SPEED_PPS * frame_time
        self.x += distance
        if self.y > self.GROUND_LINE:
            distance = self.FLYING_Y_SPEED_PPS * frame_time
            self.y -= distance
        if self.x > 700:
            self.state = self.LEFT_STAND
            self.trigger_enter = False
            self.trigger_ready = True
            self.ready_start_time = get_time()


    # 전투 준비
    def ready(self, frame_time):
        self.ready_time = get_time() - self.ready_start_time
        self.gap_time = 0.2
        if self.ready_time >= (self.gap_time * 1) and self.ready_time < (self.gap_time * 2):
            self.state = self.READY
        elif self.ready_time >= (self.gap_time * 3) and self.ready_time < (self.gap_time * 4):
            self.ready_frame = 1
        elif self.ready_time >= (self.gap_time * 4) and self.ready_time < (self.gap_time * 5):
            self.ready_frame = 2
        elif self.ready_time >= (self.gap_time * 5) and self.ready_time < (self.gap_time * 6):
            self.ready_frame = 3
        elif self.ready_time >= (self.gap_time * 6) and self.ready_time < (self.gap_time * 12):
            self.ready_frame = 2
        elif self.ready_time >= (self.gap_time * 12):
            self.state = self.LEFT_STAND
            self.dir = self.LEFT_DIR
            self.trigger_ready = False
            self.trigger_take_off = True

    # 이륙
    def take_off(self, frame_time):

        distance = self.FLYING_X_SPEED_PPS * frame_time
        # 왼쪽 방향일때 왼쪽 이륙
        if self.dir == self.LEFT_DIR:
            self.x -= distance
            self.state = self.LEFT_RUN
            if self.x < self.X_LEFT_TAKEOFF_START:
                distance = self.FLYING_Y_SPEED_PPS * frame_time
                self.y += distance
                self.state = self.LEFT_TAKE_OFF
                if self.x < self.X_LEFT_FLYING_STOP:
                    self.trigger_take_off = False
                    self.trigger_flying = True
                    self.ready_start_time = get_time()
                    self.state = self.RIGHT_FLYING
                    self.dir = self.RIGHT_DIR
                    self.y = self.Y_FLYING_START
        # 오른쪽 방향일때 오른쪽 이륙
        elif self.dir == self.RIGHT_DIR:
            self.x += distance
            self.state = self.RIGHT_RUN
            if self.x > self.X_RIGHT_TAKEOFF_START:
                distance = self.FLYING_Y_SPEED_PPS * frame_time
                self.y += distance
                self.state = self.RIGHT_TAKE_OFF
                if self.x > self.X_RIGHT_FLYING_STOP:
                    self.trigger_take_off = False
                    self.trigger_flying = True
                    self.ready_start_time = get_time()
                    self.state = self.LEFT_FLYING
                    self.dir = self.LEFT_DIR
                    self.y = self.Y_FLYING_START

    # 비행
    def flying(self, frame_time):
        self.ready_time = get_time() - self.ready_start_time
        self.gap_time = 1
        if self.ready_time >= (self.gap_time * 0) and self.ready_time < (self.gap_time * 1):
            pass
        else:
            distance = self.BOMBING_X_SPEED_PPS * frame_time
            # 왼쪽 방향 이동
            if self.dir == self.LEFT_DIR:
                self.x -= distance
                if self.x < self.X_LEFT_FLYING_STOP:
                    self.trigger_flying = False
                    # 랜덤으로 폭격, 미사일공격 패턴으로 넘어간다
                    if random.randint(1, 2) == 1:
                        self.state = self.RIGHT_BOMBING
                        self.trigger_bombing = True
                    else:
                        self.state = self.RIGHT_MISSILE
                        self.trigger_missile = True
                    self.ready_start_time = get_time()
                    self.y = random.randint(300,800)
                    self.dir = self.RIGHT_DIR    # 우측방향으로 수정
            # 오른쪽 방향 이동
            elif self.dir == self.RIGHT_DIR:
                self.x += distance
                if self.x > self.X_RIGHT_FLYING_STOP:
                    self.trigger_flying = False
                    if random.randint(1, 1) == 1:
                        self.state = self.LEFT_BOMBING
                        self.trigger_bombing = True
                    else:
                        self.state = self.LEFT_MISSILE
                        self.trigger_missile = True
                    self.ready_start_time = get_time()
                    self.y = random.randint(300, 800)
                    self.dir = self.LEFT_DIR  # 좌측방향으로 수정

    #########################
    # 미사일 공격
    def missile_attack(self, frame_time, player):
        self.ready_time = get_time() - self.ready_start_time
        self.gap_time = 1

        if self.ready_time >= (self.gap_time * 0) and self.ready_time < (self.gap_time * 1):
            self.jetman_missile = None
            #pass

        elif self.ready_time >= (self.gap_time * 1) and self.ready_time < (self.gap_time * 3):
            self.rock_total_frames += self.FRAMES_PER_ACTION * self.ROCK_PER_TIME * frame_time
            self.rock_frame = int(self.rock_total_frames) % self.ROCK_ANI_NUM
            self.rock_state = True
            self.rock_x, self.rock_y = player.x, player.y + 10
        elif self.ready_time >= (self.gap_time * 3) and self.ready_time < (self.gap_time * 4):
            self.rock_total_frames += self.FRAMES_PER_ACTION * self.ROCK_PER_TIME * frame_time * 2
            self.rock_frame = int(self.rock_total_frames) % self.ROCK_ANI_NUM
            self.rock_state = True
            self.rock_x, self.rock_y = player.x, player.y + 10
        elif self.ready_time >= (self.gap_time * 4) and self.ready_time < (self.gap_time * 5):
            self.rock_state = False
            if self.jetman_missile == None:
                self.jetman_missile = JetMan_Missile(self, player)
        elif self.ready_time >= (self.gap_time * 5):
            self.trigger_missile = False
            self.trigger_landing = True
            self.y = self.Y_LANDING_START
            self.ready_start_time = get_time()
            if self.state == self.LEFT_MISSILE:
                self.state = self.LEFT_LANDING
            elif self.state == self.RIGHT_MISSILE:
                self.state = self.RIGHT_LANDING


    # 폭격
    def bombing(self, frame_time):
        self.ready_time = get_time() - self.ready_start_time
        self.gap_time = 1
        if self.ready_time >= (self.gap_time * 0) and self.ready_time < (self.gap_time * 1):
            pass
        else:
            distance = self.BOMBING_X_SPEED_PPS * frame_time
            self.y = self.Y_FLYING_START
            if self.dir == self.LEFT_DIR:
                self.x -= distance
                if self.x < 800 and len(self.jetman_bomb_list) == 0:
                    self.jetman_bomb_list.append(JetMan_Bomb(self))
                elif self.x < 600 and len(self.jetman_bomb_list) == 1:
                    self.jetman_bomb_list.append(JetMan_Bomb(self))
                elif self.x < 400 and len(self.jetman_bomb_list) == 2:
                    self.jetman_bomb_list.append(JetMan_Bomb(self))
                elif self.x < 200 and len(self.jetman_bomb_list) == 3:
                    self.jetman_bomb_list.append(JetMan_Bomb(self))

                if self.x < self.X_LEFT_FLYING_STOP:
                    self.trigger_bombing = False
                    self.trigger_landing = True
                    self.state = self.RIGHT_LANDING
                    self.x = self.X_LEFT_FLYING_STOP
                    self.y = self.Y_LANDING_START
                    self.dir = self.RIGHT_DIR
                    self.ready_start_time = get_time()
            elif self.dir == self.RIGHT_DIR:
                self.x += distance
                if self.x > self.X_RIGHT_FLYING_STOP:
                    self.trigger_bombing = False
                    self.trigger_landing = True
                    self.state = self.LEFT_LANDING
                    self.x = self.X_RIGHT_FLYING_STOP
                    self.y = self.Y_LANDING_START
                    self.dir = self.LEFT_DIR
                    self.ready_start_time = get_time()

    # 착륙
    def landing(self, frame_time):
        self.ready_time = get_time() - self.ready_start_time
        self.gap_time = 1
        if self.ready_time >= (self.gap_time * 0) and self.ready_time < (self.gap_time * 1):
            pass
        else:
            distance = self.FLYING_X_SPEED_PPS * frame_time

            if self.dir == self.LEFT_DIR:
                self.x -= distance
                if self.y > self.GROUND_LINE:
                    distance = self.FLYING_Y_SPEED_PPS * frame_time
                    self.y -= distance
                if self.x < self.X_LEFT_LANDING_STOP:
                    self.state = self.RIGHT_STAND
                    self.trigger_landing = False
                    self.trigger_jump = True
                    self.dir = self.RIGHT_DIR
                    self.ready_start_time = get_time()

            elif self.dir == self.RIGHT_DIR:
                self.x += distance
                if self.y > self.GROUND_LINE:
                    distance = self.FLYING_Y_SPEED_PPS * frame_time
                    self.y -= distance
                if self.x > self.X_RIGHT_LANDING_STOP:
                    self.state = self.LEFT_STAND
                    self.trigger_landing = False
                    self.trigger_jump = True
                    self.dir = self.LEFT_DIR
                    self.ready_start_time = get_time()


    # 점프 공격
    def jump(self, frame_time, player):
        gap_time = 0.1
        start_gap_time = 0.5
        self.ready_time = get_time() - self.ready_start_time
        distance = 0

        if self.dir == self.LEFT_DIR:
            # 점프
            if self.ready_time >= start_gap_time and self.ready_time < gap_time + start_gap_time:
                distance = self.JUMP_POWER * frame_time
                self.state = self.LEFT_JUMP
                self.jump_frame = 0
                self.jetman_missile = None
            elif self.ready_time >= gap_time + start_gap_time and self.ready_time < gap_time*2 + start_gap_time:
                distance = self.JUMP_POWER * frame_time / 2
                self.jump_frame = 1
            elif self.ready_time >= gap_time*2 + start_gap_time and self.ready_time < gap_time*3 + start_gap_time:
                distance = self.JUMP_POWER * frame_time / 4
                self.jump_frame = 2
            elif self.ready_time >= gap_time*3 + start_gap_time and self.ready_time < gap_time*4 + start_gap_time:
                distance = self.JUMP_POWER * frame_time / 6
                self.jump_frame = 3
                if self.jetman_missile == None:
                    self.jetman_missile = JetMan_Missile(self, player)
            # 추락
            elif self.ready_time >= gap_time * 4 + start_gap_time and self.ready_time < gap_time * 5 + start_gap_time:
                distance = -(self.JUMP_POWER * frame_time / 6)
            elif self.ready_time >= gap_time * 5 + start_gap_time and self.ready_time < gap_time * 6 + start_gap_time:
                distance = -(self.JUMP_POWER * frame_time / 4)
            elif self.ready_time >= gap_time * 6 + start_gap_time and self.ready_time < gap_time * 7 + start_gap_time:
                distance = -(self.JUMP_POWER * frame_time / 2)
            elif self.ready_time >= gap_time * 7 + start_gap_time and self.ready_time < gap_time * 8 + start_gap_time:
                distance = -(self.JUMP_POWER * frame_time)
            elif self.ready_time >= gap_time * 8 + start_gap_time and self.ready_time < gap_time * 8 + start_gap_time * 2:
                self.state = self.LEFT_STAND
            elif self.ready_time >= gap_time * 8 + start_gap_time * 2:
                self.trigger_jump = False
                self.trigger_take_off = True
                self.state = self.LEFT_RUN
                self.y = self.GROUND_LINE

        elif self.dir == self.RIGHT_DIR:
            # 점프
            if self.ready_time >= start_gap_time and self.ready_time < gap_time + start_gap_time:
                distance = self.JUMP_POWER * frame_time
                self.state = self.RIGHT_JUMP
                self.jump_frame = 0
                self.jetman_missile = None
            elif self.ready_time >= gap_time + start_gap_time and self.ready_time < gap_time * 2 + start_gap_time:
                distance = self.JUMP_POWER * frame_time / 2
                self.jump_frame = 1
            elif self.ready_time >= gap_time * 2 + start_gap_time and self.ready_time < gap_time * 3 + start_gap_time:
                distance = self.JUMP_POWER * frame_time / 4
                self.jump_frame = 2
            elif self.ready_time >= gap_time * 3 + start_gap_time and self.ready_time < gap_time * 4 + start_gap_time:
                distance = self.JUMP_POWER * frame_time / 6
                self.jump_frame = 3
                if self.jetman_missile == None:
                    self.jetman_missile = JetMan_Missile(self, player)
            # 추락
            elif self.ready_time >= gap_time * 4 + start_gap_time and self.ready_time < gap_time * 5 + start_gap_time:
                distance = -(self.JUMP_POWER * frame_time / 6)
            elif self.ready_time >= gap_time * 5 + start_gap_time and self.ready_time < gap_time * 6 + start_gap_time:
                distance = -(self.JUMP_POWER * frame_time / 4)
            elif self.ready_time >= gap_time * 6 + start_gap_time and self.ready_time < gap_time * 7 + start_gap_time:
                distance = -(self.JUMP_POWER * frame_time / 2)
            elif self.ready_time >= gap_time * 7 + start_gap_time and self.ready_time < gap_time * 8 + start_gap_time:
                distance = -(self.JUMP_POWER * frame_time)
            elif self.ready_time >= gap_time * 8 + start_gap_time and self.ready_time < gap_time * 8 + start_gap_time * 2:
                self.state = self.RIGHT_STAND
            elif self.ready_time >= gap_time * 8 + start_gap_time * 2:
                self.trigger_jump = False
                self.trigger_take_off = True
                self.state = self.RIGHT_RUN
                self.y = self.GROUND_LINE
        self.y += distance

    # 사망
    def dead(self, frame_time):
        pass

    def get_bb(self):
        pass

    def draw_bb(self):
        pass

    def update(self, frame_time, player):
        self.total_frames += self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % self.SPRITE_ANIMATION_NUM

        if self.trigger_enter == True:
            self.enter_stage(frame_time)
        elif self.trigger_ready == True:
            self.ready(frame_time)
        elif self.trigger_take_off == True:
            self.take_off(frame_time)
        elif self.trigger_flying == True:
            self.flying(frame_time)
        elif self.trigger_landing == True:
            self.landing(frame_time)
        elif self.trigger_bombing == True:
            self.bombing(frame_time)
        elif self.trigger_jump == True:
            self.jump(frame_time, player)
        elif self.trigger_missile == True:
            self.missile_attack(frame_time, player)

        if self.jetman_missile:
            self.jetman_missile.update(frame_time)

        if self.jetman_bomb_list:
            for bomb in self.jetman_bomb_list:
                bomb.update(frame_time)

        #self.move(frame_time)

    def draw(self):
        if self.state == self.LEFT_STAND:
            self.image.clip_draw(self.IMAGE_SIZE * self.frame, self.IMAGE_SIZE * 6, self.IMAGE_SIZE, self.IMAGE_SIZE,
                                 self.x, self.y, self.X_SIZE, self.Y_SIZE)
        elif self.state == self.RIGHT_STAND:
            self.image.clip_draw(self.IMAGE_SIZE * self.frame, self.IMAGE_SIZE * 7, self.IMAGE_SIZE, self.IMAGE_SIZE,
                                 self.x, self.y, self.X_SIZE, self.Y_SIZE)
        elif self.state in (self.LEFT_LANDING, self.LEFT_RUN):
            self.image.clip_draw(self.IMAGE_SIZE * self.frame, self.IMAGE_SIZE * 4, self.IMAGE_SIZE, self.IMAGE_SIZE,
                                 self.x, self.y, self.X_SIZE, self.Y_SIZE)
        elif self.state in (self.RIGHT_LANDING, self.RIGHT_RUN):
            self.image.clip_draw(self.IMAGE_SIZE * self.frame, self.IMAGE_SIZE * 5, self.IMAGE_SIZE, self.IMAGE_SIZE,
                                 self.x, self.y, self.X_SIZE, self.Y_SIZE)
        elif self.state in (self.LEFT_TAKE_OFF, self.LEFT_FLYING, self.LEFT_BOMBING):
            self.image.clip_draw(self.IMAGE_SIZE * self.frame, self.IMAGE_SIZE * 2, self.IMAGE_SIZE, self.IMAGE_SIZE,
                                 self.x, self.y, self.X_SIZE, self.Y_SIZE)
        elif self.state in (self.RIGHT_TAKE_OFF, self.RIGHT_FLYING, self.RIGHT_BOMBING):
            self.image.clip_draw(self.IMAGE_SIZE * self.frame, self.IMAGE_SIZE * 3, self.IMAGE_SIZE, self.IMAGE_SIZE,
                                 self.x, self.y, self.X_SIZE, self.Y_SIZE)
        elif self.state in (self.LEFT_JUMP, ):
            self.image.clip_draw(self.IMAGE_SIZE * self.jump_frame, self.IMAGE_SIZE * 0, self.IMAGE_SIZE, self.IMAGE_SIZE,
                                 self.x, self.y, self.X_SIZE, self.Y_SIZE)
        elif self.state in (self.RIGHT_JUMP, ):
            self.image.clip_draw(self.IMAGE_SIZE * self.jump_frame, self.IMAGE_SIZE * 1, self.IMAGE_SIZE, self.IMAGE_SIZE,
                                 self.x, self.y, self.X_SIZE, self.Y_SIZE)
        # 미사일 공격
        elif self.state in (self.LEFT_MISSILE, self.RIGHT_MISSILE) and self.rock_state == True:
            self.rock_on_image.clip_draw(self.ROCK_IMAGE_SIZE * self.rock_frame, 0, self.ROCK_IMAGE_SIZE, self.ROCK_IMAGE_SIZE,
                                 self.rock_x, self.rock_y, self.ROCK_SIZE, self.ROCK_SIZE)

        elif self.state == self.READY:
            self.image.clip_draw(self.IMAGE_SIZE * self.ready_frame, self.IMAGE_SIZE * 8, self.IMAGE_SIZE, self.IMAGE_SIZE,
                                 self.x, self.y, self.X_SIZE, self.Y_SIZE)
        if self.jetman_missile:
            self.jetman_missile.draw()
        if self.jetman_bomb_list:
            for bomb in self.jetman_bomb_list:
                bomb.draw()
