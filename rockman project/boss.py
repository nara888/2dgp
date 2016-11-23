import sys
sys.path.append('../LabsAll/Labs')

from pico2d import *

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


    LANDING_Y_SPEED_PPS = FLYING_Y_SPEED_PPS * 0.7

    TIME_PER_ACTION = 2
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    IMAGE_SIZE = 60

    X_SIZE = 180
    Y_SIZE = X_SIZE
    SPRITE_ANIMATION_NUM = 2
    image = None

    RIGHT_STAND, LEFT_STAND, RIGHT_RUN, LEFT_RUN, RIGHT_FLYING, LEFT_FLYING, \
    RIGHT_LANDING, LEFT_LANDING, RIGHT_TAKE_OFF, LEFT_TAKE_OFF, \
    RIGHT_JUMP, LEFT_JUMP, RIGHT_FALL, LEFT_FALL, READY \
        = 0,1,2,3,4,5,6,7,8,9,10,11,12,13, 14

    def __init__(self):
        if self.image == None:
            self.image = load_image('resource/boss/jetman/jetman_240x540.png')

        self.x, self.y = 0, 300
        self.dir = 1
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
        self.ready_time = 0
        self.ready_start_time = 0
        self.ready_frame = 0

    # 스테이지 등장
    def enter_stage(self, frame_time):
        distance = self.FLYING_X_SPEED_PPS * frame_time
        self.x += distance
        if self.y > 150:
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
            self.dir = -1
            self.trigger_ready = False
            self.trigger_take_off = True

    # 이륙
    def take_off(self, frame_time):
        distance = self.FLYING_X_SPEED_PPS * frame_time
        # 왼쪽 방향일때 왼쪽 이륙
        if self.dir == -1:
            self.x -= distance
            self.state = self.LEFT_RUN
            if self.x < 250:
                distance = self.FLYING_Y_SPEED_PPS * frame_time
                self.y += distance
                self.state = self.LEFT_TAKE_OFF
                if self.x < -100:
                    self.trigger_take_off = False
                    self.trigger_flying = True
                    self.ready_start_time = get_time()
                    self.state = self.RIGHT_FLYING
                    self.dir = 1
                    self.y = 600

    # 착륙
    def landing(self, frame_time):
        distance = self.FLYING_X_SPEED_PPS * frame_time
        self.x -= distance
        if self.y > 150:
            distance = self.LANDING_Y_SPEED_PPS * frame_time
            self.y -= distance
        if self.x < 100:
            self.state = self.RIGHT_STAND
            self.trigger_landing = False
            self.trigger_jump = True

    # 비행
    def flying(self, frame_time):
        self.ready_time = get_time() - self.ready_start_time
        self.gap_time = 1
        if self.ready_time >= (self.gap_time * 0) and self.ready_time < (self.gap_time * 1):
            pass
        else:
            distance = self.FLYING_X_SPEED_PPS * frame_time
            self.x += distance
            if self.x > 900:
                self.trigger_flying = False
                self.trigger_landing = True
                self.state = self.LEFT_LANDING
                self.y = 300

    # 이동
    def move(self, frame_time):
        #distance = self.RUN_SPEED_PPS * frame_time
        #self.x += (self.dir * distance)
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
        elif self.state in (self.LEFT_TAKE_OFF, self.LEFT_FLYING):
            self.image.clip_draw(self.IMAGE_SIZE * self.frame, self.IMAGE_SIZE * 2, self.IMAGE_SIZE, self.IMAGE_SIZE,
                                 self.x, self.y, self.X_SIZE, self.Y_SIZE)
        elif self.state in (self.RIGHT_TAKE_OFF, self.RIGHT_FLYING):
            self.image.clip_draw(self.IMAGE_SIZE * self.frame, self.IMAGE_SIZE * 3, self.IMAGE_SIZE, self.IMAGE_SIZE,
                                 self.x, self.y, self.X_SIZE, self.Y_SIZE)
        elif self.state == self.READY:
            self.image.clip_draw(self.IMAGE_SIZE * self.ready_frame, self.IMAGE_SIZE * 8, self.IMAGE_SIZE, self.IMAGE_SIZE,
                                 self.x, self.y, self.X_SIZE, self.Y_SIZE)
