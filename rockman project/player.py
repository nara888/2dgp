import sys
sys.path.append('../LabsAll/Labs')

from pico2d import *
from player_bullet import Bullet
from sound_manager import *

class Player:

    CHAR_SIZE = 120
    DEAD_EFFECT_SIZE = 80
    ENTER_EFFECT_YSIZE = 100
    ENTER_EFFECT_XSIZE = ENTER_EFFECT_YSIZE * 0.85

    PIXEL_PER_METER = (10.0 / 0.3)              # 10 pixel 30 cm
    RUN_SPEED_KMPH = 27.0                       # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    SLIDING_SPEED_KMPH = 50.0  # Km / Hour
    SLIDING_SPEED_MPM = (SLIDING_SPEED_KMPH * 1000.0 / 60.0)
    SLIDING_SPEED_MPS = (SLIDING_SPEED_MPM / 60.0)
    SLIDING_SPEED_PPS = (SLIDING_SPEED_MPS * PIXEL_PER_METER)

    FALL_SPEED_KMPH = 40.0  # Km / Hour
    FALL_SPEED_MPM = (FALL_SPEED_KMPH * 1000.0 / 60.0)
    FALL_SPEED_MPS = (FALL_SPEED_MPM / 60.0)
    FALL_SPEED_PPS = (FALL_SPEED_MPS * PIXEL_PER_METER)

    DEAD_EFFECT_SPEED_KMPH = 30.0
    DEAD_EFFECT_SPEED_MPM = (DEAD_EFFECT_SPEED_KMPH * 1000.0 / 60.0)
    DEAD_EFFECT_SPEED_MPS = (DEAD_EFFECT_SPEED_MPM / 60.0)
    DEAD_EFFECT_SPEED_PPS = (DEAD_EFFECT_SPEED_MPS * PIXEL_PER_METER)

    ENTER_SPEED_KMPH = 100.0  # Km / Hour
    ENTER_SPEED_MPM = (ENTER_SPEED_KMPH * 1000.0 / 60.0)
    ENTER_SPEED_MPS = (ENTER_SPEED_MPM / 60.0)
    ENTER_SPEED_PPS = (ENTER_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 1.0
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    TIME_PER_DEAD_EFFECT = 0.5
    DEAD_EFFECT_PER_TIME = 1.0 / TIME_PER_DEAD_EFFECT
    FRAMES_PER_DEAD_EFFECT = 8

    TIME_PER_LANDING_EFFECT = 0.5
    LANDING_EFFECT_PER_TIME = 1.0 / TIME_PER_LANDING_EFFECT
    FRAMES_PER_LANDING_EFFECT = 8

    TIME_PER_READY = 5.0
    READY_PER_TIME = 1.0 / TIME_PER_READY
    FRAMES_PER_READY = 8

    TIME_PER_HIT = 0.3
    HIT_PER_TIME = 1.0 / TIME_PER_HIT

    STAND_BB_WIDTH = 25
    STAND_BB_HEIGHT = 30

    MAX_HP = 28

    STOP_TIME = 2

    player_image = None
    dead_effect_image = None
    enter_effect_image = None
    ready_text_image = None

    ready_text_image_width = 114
    ready_text_image_height = 21
    ready_text_width = ready_text_image_width
    ready_text_height = ready_text_image_height

    LEFT_RUN, RIGHT_RUN, LEFT_STAND, RIGHT_STAND, \
    LEFT_JUMP, RIGHT_JUMP, LEFT_SLIDING, RIGHT_SLIDING, LEFT_FALL, RIGHT_FALL, \
    LEFT_MOVE_JUMP, RIGHT_MOVE_JUMP, LEFT_MOVE_FALL, RIGHT_MOVE_FALL, \
    ENTER_STAGE, ESCAPE_STAGE, LANDING_STAGE, READY, STOP, DEAD, \
    LEFT_DAMAGED, RIGHT_DAMAGED, TAKE_OFF_STAGE, ESCAPE_STAGE \
        = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23

    def __init__(self):
        self.x, self.y = 100, 800
        self.dir = 1
        self.total_frames = 0.0
        self.total_dead_frames = 0.0
        self.total_landing_frames = 0.0
        self.frame = 0
        self.dead_frame = 0
        self.landing_frame = 0
        self.hp = self.MAX_HP
        self.state = self.READY  # 플레이어 상태
        self.shot_state = False     # 샷 상태
        self.action_start_time = get_time()  # 점프, 슬라이딩 시작 시간
        self.shot_start_time = 0    # 샷 시작 시간
        self.accel = 850  # 점프 가속
        self.ground_y = 70 + self.CHAR_SIZE / 2

        self.left_key_state = False  # 좌측 키 누름 상태
        self.right_key_state = False # 우측 키 누름 상태

        self.enter_trigger = False
        self.clear_trigger = False
        self.escape_trigger = False
        self.end_state = False

        self.hit_state = False  # 맞은 상태인가
        self.hit_start_time = 0  # 맞기 시작시간
        self.hit_total_frames = 0
        self.hit_frame = 0

        self.bullet_list = []

        self.clear_state = False

        self.sound_manager = None

        self.dead_r = 0
        self.dead_r2 = 0
        self.dead_effect_xpos = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.dead_effect_ypos = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.dead_effect_xpos2 = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.dead_effect_ypos2 = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.dead_effect_degree = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        if Player.player_image == None:
            Player.player_image = load_image('resource/rockman/rockman240x280.png')
        if Player.dead_effect_image == None:
            Player.dead_effect_image = load_image('resource/effect/small_explosion_effect_400x80.png')
        if Player.enter_effect_image == None:
            Player.enter_effect_image = load_image('resource/rockman/enter_effect_90x35.png')
        if Player.ready_text_image == None:
            Player.ready_text_image = load_image('resource/ui/ready_text.png')

    # 레디
    def ready(self, frame_time):
        if get_time() - self.action_start_time > self.STOP_TIME:  # 0.x초를 지나면 상태 변경
            self.state = self.ENTER_STAGE

    # 스테이지 워프
    def enter_stage(self, frame_time):
        if self.y < self.ground_y:
            self.y = self.ground_y
            self.action_start_time = get_time()
            self.state = self.LANDING_STAGE
        else:
            distance = Player.ENTER_SPEED_PPS * frame_time
            self.y -= distance


    # 워프 착지
    def landing_stage(self, frame_time):
        if self.enter_trigger == False:
            self.sound_manager.enter_stage()
            self.enter_trigger = True
        if get_time() - self.action_start_time > 0.1:  # 0.x초를 지나면 상태 변경
            self.state = self.STOP
            self.action_start_time = get_time()
            self.enter_trigger = False


    # 워프 준비
    def take_off_stage(self, frame_time):
        if self.enter_trigger == False:
            self.sound_manager.out_stage()
            self.enter_trigger = True
        if get_time() - self.action_start_time > 0.1:  # 0.x초를 지나면 상태 변경
            self.state = self.ESCAPE_STAGE
            self.action_start_time = get_time()
            self.enter_trigger = False

    # 스테이지 탈출
    def escape_stage(self, frame_time):
        if self.y > 850:
            self.end_state = True
        else:
            distance = Player.ENTER_SPEED_PPS * frame_time
            self.y += distance


    # 정지
    def stop(self, frame_time):
        if get_time() - self.action_start_time > self.STOP_TIME:  # 0.x초를 지나면 상태 변경
            if self.right_key_state == True:
                self.state = self.RIGHT_RUN
            elif self.left_key_state == True:
                self.state = self.LEFT_RUN
            else:
                self.state = self.RIGHT_STAND

    # 이동
    def move(self, frame_time):
        distance = Player.RUN_SPEED_PPS * frame_time
        self.x += (self.dir * distance)

    # 슬라이딩
    def sliding(self, frame_time):
        distance = Player.SLIDING_SPEED_PPS * frame_time
        self.x += (self.dir * distance)

        if get_time() - self.action_start_time > 0.4:  # 슬라이딩 시간이 0.x초를 지나면 상태 변경
            if self.state == self.RIGHT_SLIDING:
                if self.right_key_state == True:       # 우측 키를 누른 상태이면 RUN 으로, 아니라면 STAND로 상태 변경
                    self.state = self.RIGHT_RUN
                else:
                    self.state = self.RIGHT_STAND
            elif self.state == self.LEFT_SLIDING:
                if self.left_key_state == True:
                    self.state = self.LEFT_RUN
                else:
                    self.state = self.LEFT_STAND
            self.action_start_time = 0

    # 점프

    def jump(self, frame_time):
        gap_time = 0.1
        if get_time() - self.action_start_time < 0.1:
            distance = self.accel * frame_time
        elif get_time() - self.action_start_time >= gap_time and get_time() - self.action_start_time < gap_time*2:
            distance = self.accel * frame_time / 2
        elif get_time() - self.action_start_time >= gap_time*2 and get_time() - self.action_start_time < gap_time*3:
            distance = self.accel * frame_time / 4
        elif get_time() - self.action_start_time >= gap_time*3:
            distance = self.accel * frame_time / 6


        self.y += distance

        # 이동점프 중이면 x값을 변경
        if self.state in (self.LEFT_MOVE_JUMP, self.RIGHT_MOVE_JUMP):
            distance = Player.RUN_SPEED_PPS * frame_time
            self.x += (self.dir * distance)

        if get_time() - self.action_start_time > gap_time*3.5:  # 점프 시간이 0.x초를 지나면 낙하로 상태 변경
            self.action_start_time = get_time()
            if self.state in (self.LEFT_JUMP,):
                self.state = self.LEFT_FALL
            elif self.state in (self.RIGHT_JUMP,):
                self.state = self.RIGHT_FALL
            elif self.state in (self.LEFT_MOVE_JUMP,):
                self.state = self.LEFT_MOVE_FALL
            elif self.state in (self.RIGHT_MOVE_JUMP,):
                self.state = self.RIGHT_MOVE_FALL


    # 낙하

    def fall(self, frame_time):
        if self.y < self.ground_y:
            self.y = self.ground_y
            self.action_start_time = 0
            self.sound_manager.jump()
            if self.state in (self.LEFT_FALL,):
                self.state = self.LEFT_STAND
            elif self.state in (self.RIGHT_FALL,):
                self.state = self.RIGHT_STAND
            elif self.state in (self.LEFT_MOVE_FALL,):
                self.state = self.LEFT_RUN
            elif self.state in (self.RIGHT_MOVE_FALL,):
                self.state = self.RIGHT_RUN

        else:
            gap_time = 0.1
            if get_time() - self.action_start_time < gap_time*0.5:
                distance = self.accel * frame_time / 6
            elif get_time() - self.action_start_time >= gap_time*0.5 and get_time() - self.action_start_time < gap_time * 1.5:
                distance = self.accel * frame_time / 4
            elif get_time() - self.action_start_time >= gap_time * 1.5 and get_time() - self.action_start_time < gap_time * 2.5:
                distance = self.accel * frame_time / 2
            elif get_time() - self.action_start_time >= gap_time * 2.5:
                distance = self.accel * frame_time

            self.y -= distance
            # 이동낙하 중이면 x값을 변경
            if self.state in (self.LEFT_MOVE_FALL, self.RIGHT_MOVE_FALL):
                distance = Player.RUN_SPEED_PPS * frame_time
                self.x += (self.dir * distance)

    # 발사
    def shot(self, frame_time):
        if get_time() - self.shot_start_time > 0.3:  # 샷을 쏜 시간이 0.x초 지나면 shot_state를 False로 바꾼다
            self.shot_start_time = 0
            self.shot_state = False

    # 사망
    def dead(self, frame_time):
        distance = Player.DEAD_EFFECT_SPEED_PPS * frame_time
        self.dead_r = self.dead_r + distance
        distance = Player.DEAD_EFFECT_SPEED_PPS * frame_time * 2
        self.dead_r2 = self.dead_r2 + distance

        for i in range(0, 8):
            radian = self.dead_effect_degree[i] * 3.141592 / 180

            self.dead_effect_xpos[i] = self.x + self.dead_r * math.cos(radian)
            self.dead_effect_ypos[i] = self.y + self.dead_r * math.sin(radian)
            self.dead_effect_xpos2[i] = self.x + self.dead_r2 * math.cos(radian)
            self.dead_effect_ypos2[i] = self.y + self.dead_r2 * math.sin(radian)

        if get_time() - self.action_start_time > 4:
            self.end_state = True

    def hit_check(self):
        return self.hit_state

    # 데미지
    def damaged(self, frame_time, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.state = self.DEAD
            self.action_start_time = get_time()
            self.sound_manager.dead()
            for i in range(0, 8):
                self.dead_effect_xpos[i] = self.x
                self.dead_effect_ypos[i] = self.y
                self.dead_effect_xpos2[i] = self.x
                self.dead_effect_ypos2[i] = self.y
                self.dead_effect_degree[i] = 45 * i
            return
        self.hit_state = True  # 맞은 상태인가
        if self.dir == 1:
            self.state = self.RIGHT_DAMAGED
        elif self.dir == -1:
            self.state = self.LEFT_DAMAGED
        self.hit_start_time = get_time()
        self.action_start_time = get_time()
        self.sound_manager.damaged()

    # 무적시간 해제
    def hit_recovery(self, frame_time):
        if self.y < self.ground_y and self.state in (self.LEFT_DAMAGED, self.RIGHT_DAMAGED):
            self.y = self.ground_y
            distance = Player.RUN_SPEED_PPS * frame_time / 2
            self.x -= (self.dir * distance)
        elif self.y >= self.ground_y and self.state in (self.LEFT_DAMAGED, self.RIGHT_DAMAGED):
            gap_time = 0.1
            if get_time() - self.action_start_time < gap_time*0.5:
                distance = self.accel * frame_time / 6
            elif get_time() - self.action_start_time >= gap_time*0.5 and get_time() - self.action_start_time < gap_time * 1.5:
                distance = self.accel * frame_time / 4
            elif get_time() - self.action_start_time >= gap_time * 1.5 and get_time() - self.action_start_time < gap_time * 2.5:
                distance = self.accel * frame_time / 2
            elif get_time() - self.action_start_time >= gap_time * 2.5:
                distance = self.accel * frame_time

            self.y -= distance
            distance = Player.RUN_SPEED_PPS * frame_time / 3
            self.x -= (self.dir * distance)


        if self.hit_state and get_time() - self.hit_start_time > 0.5:
            if self.dir == 1 and self.state == self.RIGHT_DAMAGED:
                if self.right_key_state == True:  # 우측 키를 누른 상태이면 RUN 으로, 아니라면 STAND로 상태 변경
                    self.state = self.RIGHT_RUN
                else:
                    self.state = self.RIGHT_STAND
            elif self.dir == -1 and self.state == self.LEFT_DAMAGED:
                if self.left_key_state == True:
                    self.state = self.LEFT_RUN
                else:
                    self.state = self.LEFT_STAND
        if get_time() - self.hit_start_time > 2.0:
            self.hit_state = False


    def get_bb(self):
        if self.state in (self.LEFT_SLIDING, self.RIGHT_SLIDING):
            return self.x - Player.STAND_BB_WIDTH, self.y - Player.STAND_BB_HEIGHT, self.x + Player.STAND_BB_WIDTH, self.y + Player.STAND_BB_HEIGHT - 15
        else:
            return self.x - Player.STAND_BB_WIDTH, self.y - Player.STAND_BB_HEIGHT, self.x + Player.STAND_BB_WIDTH, self.y + Player.STAND_BB_HEIGHT

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def get_clear_state(self):
        self.clear_state = True


    def handle_event(self, event):

        # 왼쪽 방향키 입력
        if(event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
            self.left_key_state = True

            if self.state in (self.RIGHT_STAND, self.LEFT_STAND, self.RIGHT_RUN, self.LEFT_SLIDING, self.RIGHT_SLIDING):
                self.state = self.LEFT_RUN
                self.dir = -1
            elif self.state in (self.LEFT_JUMP, self.RIGHT_JUMP, self.RIGHT_MOVE_JUMP):
                self.state = self.LEFT_MOVE_JUMP
                self.dir = -1
            elif self.state in (self.LEFT_FALL, self.RIGHT_FALL, self.RIGHT_MOVE_FALL):
                self.state = self.LEFT_MOVE_FALL
                self.dir = -1

        # 오른쪽 방향키 입력
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            self.right_key_state = True

            if self.state in (self.RIGHT_STAND, self.LEFT_STAND, self.LEFT_RUN, self.LEFT_SLIDING, self.RIGHT_SLIDING):
                self.state = self.RIGHT_RUN
                self.dir = 1
            elif self.state in (self.LEFT_JUMP, self.RIGHT_JUMP, self.LEFT_MOVE_JUMP):
                self.state = self.RIGHT_MOVE_JUMP
                self.dir = 1
            elif self.state in (self.LEFT_FALL, self.RIGHT_FALL, self.LEFT_MOVE_FALL):
                self.state = self.RIGHT_MOVE_FALL
                self.dir = 1

        # 왼쪽 방향키 뗌
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_LEFT):
            self.left_key_state = False

            if self.state in (self.LEFT_RUN, ):
                self.state = self.LEFT_STAND
            elif self.state in (self.LEFT_MOVE_JUMP, ):
                self.state = self.LEFT_JUMP
            elif self.state in (self.LEFT_MOVE_FALL, ):
                self.state = self.LEFT_FALL

        # 오른쪽 방향키 뗌
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_RIGHT):
            self.right_key_state = False

            if self.state in (self.RIGHT_RUN, ):
                self.state = self.RIGHT_STAND
            elif self.state in (self.RIGHT_MOVE_JUMP, ):
                self.state = self.RIGHT_JUMP
            elif self.state in (self.RIGHT_MOVE_FALL, ):
                self.state = self.RIGHT_FALL

        # z키 입력 : 공격
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_z):
            if self.state in (self.LEFT_SLIDING, self.RIGHT_SLIDING, self.STOP, self.ENTER_STAGE, self.LANDING_STAGE, self.LEFT_DAMAGED, self.RIGHT_DAMAGED):
                pass
            else:
                if len(self.bullet_list) < 3:  # 블릿 리스트에 블릿이 2개 이하 이면 블릿 생성
                    self.bullet_list.append(Bullet(self))
                    self.sound_manager.shot()
                self.shot_state = True
                self.shot_start_time = get_time()

        # x키 입력 : 점프
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_x):
            if self.state in (self.RIGHT_STAND, ):
                self.state = self.RIGHT_JUMP
                self.action_start_time = get_time()
            elif self.state in (self.LEFT_STAND, ):
                self.state = self.LEFT_JUMP
                self.action_start_time = get_time()
            elif self.state in (self.RIGHT_RUN, ):
                self.state = self.RIGHT_MOVE_JUMP
                self.action_start_time = get_time()
            elif self.state in (self.LEFT_RUN, ):
                self.state = self.LEFT_MOVE_JUMP
                self.action_start_time = get_time()
            elif self.state in (self.RIGHT_SLIDING, ):
                if self.right_key_state == True:
                    self.state = self.RIGHT_MOVE_JUMP
                else:
                    self.state = self.RIGHT_JUMP
                self.action_start_time = get_time()
            elif self.state in (self.LEFT_SLIDING, ):
                if self.left_key_state == True:
                    self.state = self.LEFT_MOVE_JUMP
                else:
                    self.state = self.LEFT_JUMP
                self.action_start_time = get_time()



        # x키 뗌
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_x):
            if self.state in (self.RIGHT_JUMP, ):
                self.state = self.RIGHT_FALL
                self.action_start_time = get_time()
            elif self.state in (self.LEFT_JUMP, ):
                self.state = self.LEFT_FALL
                self.action_start_time = get_time()
            elif self.state in (self.RIGHT_MOVE_JUMP, ):
                self.state = self.RIGHT_MOVE_FALL
                self.action_start_time = get_time()
            elif self.state in (self.LEFT_MOVE_JUMP, ):
                self.state = self.LEFT_MOVE_FALL
                self.action_start_time = get_time()

        # c키 입력 : 슬라이딩
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_c):
            if self.state in (self.LEFT_STAND, self.LEFT_RUN):
                self.state = self.LEFT_SLIDING
                self.action_start_time = get_time()
                self.dir = -1
            elif self.state in (self.RIGHT_STAND, self.RIGHT_RUN):
                self.state = self.RIGHT_SLIDING
                self.action_start_time = get_time()
                self.dir = 1



    def update(self, frame_time):

        self.total_frames += Player.FRAMES_PER_ACTION * Player.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 3

        if self.state in (self.LEFT_RUN, self.RIGHT_RUN):
            self.move(frame_time)
        elif self.state in (self.LEFT_SLIDING, self.RIGHT_SLIDING):
            self.sliding(frame_time)
        elif self.state in (self.LEFT_JUMP, self.RIGHT_JUMP, self.LEFT_MOVE_JUMP, self.RIGHT_MOVE_JUMP):
            self.jump(frame_time)
        elif self.state in (self.LEFT_FALL, self.RIGHT_FALL, self.LEFT_MOVE_FALL, self.RIGHT_MOVE_FALL):
            self.fall(frame_time)
        elif self.state in (self.DEAD, ):
            self.total_dead_frames += Player.FRAMES_PER_DEAD_EFFECT * Player.DEAD_EFFECT_PER_TIME * frame_time
            self.dead_frame = int(self.total_dead_frames) % 5
            self.dead(frame_time)
        elif self.state in (self.READY,):
            self.total_frames += Player.FRAMES_PER_READY * Player.READY_PER_TIME * frame_time
            self.frame = int(self.total_frames) % 2
            self.ready(frame_time)
        elif self.state in (self.ENTER_STAGE,):
            self.enter_stage(frame_time)
        elif self.state in (self.LANDING_STAGE,):
            self.total_landing_frames += Player.FRAMES_PER_LANDING_EFFECT * Player.LANDING_EFFECT_PER_TIME * frame_time
            self.landing_frame = int(self.total_landing_frames) % 5
            self.landing_stage(frame_time)
        elif self.state in (self.STOP, ):
            self.stop(frame_time)
        elif self.state in (self.TAKE_OFF_STAGE, ):
            self.take_off_stage(frame_time)
        elif self.state in (self.ESCAPE_STAGE, ):
            self.escape_stage(frame_time)

        self.x = clamp(0 + self.STAND_BB_HEIGHT, self.x, 800 - self.STAND_BB_HEIGHT)


        if self.hit_state:
            self.hit_recovery(frame_time)
            self.hit_total_frames += self.FRAMES_PER_ACTION * self.HIT_PER_TIME * frame_time
            self.hit_frame = int(self.hit_total_frames) % 2

        if self.shot_state == True:
            self.shot(frame_time)

        if self.clear_state and self.clear_trigger == False:
            if self.state == self.LEFT_RUN:
                self.state = self.LEFT_STAND
            elif self.state == self.RIGHT_RUN:
                self.state = self.RIGHT_STAND
            self.action_start_time = get_time()
            self.clear_trigger = True

        if self.clear_trigger and get_time() - self.action_start_time >= 11.0:
            self.state = self.TAKE_OFF_STAGE

        for bullet in self.bullet_list:
            bullet.update(frame_time)
            if bullet.x > 800 or bullet.x < 0:
                self.bullet_list.remove(bullet)

        print("Change Time: %f, Total Frames: %d" %(get_time(), self.total_frames))

    def draw(self):
        if self.hit_state and self.hit_frame == 0 and self.state != self.LEFT_DAMAGED and self.state != self.RIGHT_DAMAGED:
            pass

        elif self.state == self.LEFT_STAND:
            if self.shot_state == False:
                self.player_image.clip_draw(0, 200, 40, 40, self.x, self.y, Player.CHAR_SIZE, Player.CHAR_SIZE)
            else:
                self.player_image.clip_draw(0, 120, 40, 40, self.x, self.y, Player.CHAR_SIZE, Player.CHAR_SIZE)
        elif self.state == self.RIGHT_STAND or self.state == self.STOP:
            if self.shot_state == False:
                self.player_image.clip_draw(0, 240, 40, 40, self.x, self.y, Player.CHAR_SIZE, Player.CHAR_SIZE)
            else:
                self.player_image.clip_draw(0, 160, 40, 40, self.x, self.y, Player.CHAR_SIZE, Player.CHAR_SIZE)
        elif self.state == self.LEFT_RUN:
            if self.shot_state == False:
                self.player_image.clip_draw(self.frame * 40 + 40, 200, 40, 40, self.x, self.y, Player.CHAR_SIZE, Player.CHAR_SIZE)
            else:
                self.player_image.clip_draw(self.frame * 40 + 40, 120, 40, 40, self.x, self.y, Player.CHAR_SIZE, Player.CHAR_SIZE)
        elif self.state == self.RIGHT_RUN:
            if self.shot_state == False:
                self.player_image.clip_draw(self.frame * 40 + 40, 240, 40, 40, self.x, self.y, Player.CHAR_SIZE, Player.CHAR_SIZE)
            else:
                self.player_image.clip_draw(self.frame * 40 + 40, 160, 40, 40, self.x, self.y, Player.CHAR_SIZE, Player.CHAR_SIZE)
        elif self.state in (self.LEFT_JUMP, self.LEFT_MOVE_JUMP, self.LEFT_FALL, self.LEFT_MOVE_FALL):
            if self.shot_state == False:
                self.player_image.clip_draw(160, 200, 40, 40, self.x, self.y, Player.CHAR_SIZE, Player.CHAR_SIZE)
            else:
                self.player_image.clip_draw(160, 120, 40, 40, self.x, self.y, Player.CHAR_SIZE, Player.CHAR_SIZE)
        elif self.state in (self.RIGHT_JUMP, self.RIGHT_MOVE_JUMP, self.RIGHT_FALL, self.RIGHT_MOVE_FALL):
            if self.shot_state == False:
                self.player_image.clip_draw(160, 240, 40, 40, self.x, self.y, Player.CHAR_SIZE, Player.CHAR_SIZE)
            else:
                self.player_image.clip_draw(160, 160, 40, 40, self.x, self.y, Player.CHAR_SIZE, Player.CHAR_SIZE)
        elif self.state == self.LEFT_SLIDING:
            self.player_image.clip_draw(200, 200, 40, 40, self.x, self.y, Player.CHAR_SIZE, Player.CHAR_SIZE)
        elif self.state == self.RIGHT_SLIDING:
            self.player_image.clip_draw(200, 240, 40, 40, self.x, self.y, Player.CHAR_SIZE, Player.CHAR_SIZE)
        elif self.state == self.DEAD:
            for i in range(0, 8):
                self.dead_effect_image.clip_draw(self.dead_frame * 80, 0, 80, 80, self.dead_effect_xpos[i],
                                                 self.dead_effect_ypos[i], Player.DEAD_EFFECT_SIZE, Player.DEAD_EFFECT_SIZE)
                self.dead_effect_image.clip_draw(self.dead_frame * 80, 0, 80, 80, self.dead_effect_xpos2[i],
                                                 self.dead_effect_ypos2[i], Player.DEAD_EFFECT_SIZE,
                                                 Player.DEAD_EFFECT_SIZE)
        elif self.state in (self.ENTER_STAGE, self.ESCAPE_STAGE):
            self.enter_effect_image.clip_draw(0, 0, 30, 35, self.x, self.y, self.ENTER_EFFECT_XSIZE, self.ENTER_EFFECT_YSIZE)
        elif self.state in (self.LANDING_STAGE, self.TAKE_OFF_STAGE):
            self.enter_effect_image.clip_draw(self.landing_frame * 30 + 30, 0, 30, 35, self.x, self.y, self.ENTER_EFFECT_XSIZE, self.ENTER_EFFECT_YSIZE)
        elif self.state == self.READY and self.frame == 0:
            self.ready_text_image.draw(400, 400)
        elif self.state == self.LEFT_DAMAGED:
            self.player_image.clip_draw(self.hit_frame * 40, 0, 40, 40, self.x, self.y, Player.CHAR_SIZE, Player.CHAR_SIZE)
        elif self.state == self.RIGHT_DAMAGED:
            self.player_image.clip_draw(self.hit_frame * 40, 40, 40, 40, self.x, self.y, Player.CHAR_SIZE, Player.CHAR_SIZE)

        for bullet in self.bullet_list:
            bullet.draw()

    def get_bullet_list(self):
        return self.bullet_list

    def set_sound_manager(self, sm):
        self.sound_manager = sm

    def get_player_dead(self):
        if self.state == self.DEAD:
            return True
        return False

    def get_end_state(self):
        return self.end_state