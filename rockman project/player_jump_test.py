import sys
import math
sys.path.append('../LabsAll/Labs')

from pico2d import *

running = None


class Stage:
    def __init__(self):
        self.image = load_image('resource/stage/stage.png')

    def draw(self):
        self.image.draw(400, 350, 800, 700)


class Player:

    CHAR_SIZE = 120
    DEAD_EFFECT_SIZE = 80

    PIXEL_PER_METER = (10.0 / 0.3)              # 10 pixel 30 cm
    RUN_SPEED_KMPH = 27.0                       # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    SLIDING_SPEED_KMPH = 50.0  # Km / Hour
    SLIDING_SPEED_MPM = (SLIDING_SPEED_KMPH * 1000.0 / 60.0)
    SLIDING_SPEED_MPS = (SLIDING_SPEED_MPM / 60.0)
    SLIDING_SPEED_PPS = (SLIDING_SPEED_MPS * PIXEL_PER_METER)

    FALL_SPEED_KMPH = 80.0  # Km / Hour
    FALL_SPEED_MPM = (FALL_SPEED_KMPH * 1000.0 / 60.0)
    FALL_SPEED_MPS = (FALL_SPEED_MPM / 60.0)
    FALL_SPEED_PPS = (FALL_SPEED_MPS * PIXEL_PER_METER)

    DEAD_EFFECT_SPEED_KMPH = 30.0
    DEAD_EFFECT_SPEED_MPM = (DEAD_EFFECT_SPEED_KMPH * 1000.0 / 60.0)
    DEAD_EFFECT_SPEED_MPS = (DEAD_EFFECT_SPEED_MPM / 60.0)
    DEAD_EFFECT_SPEED_PPS = (DEAD_EFFECT_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 1.0
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    TIME_PER_DEAD_EFFECT = 0.5
    DEAD_EFFECT_PER_TIME = 1.0 / TIME_PER_DEAD_EFFECT
    FRAMES_PER_DEAD_EFFECT = 8

    STAND_BB_WIDTH = 25
    STAND_BB_HEIGHT = 30

    player_image = None
    dead_effect_image = None

    LEFT_RUN, RIGHT_RUN, LEFT_STAND, RIGHT_STAND, \
    LEFT_JUMP, RIGHT_JUMP, LEFT_SLIDING, RIGHT_SLIDING, LEFT_FALL, RIGHT_FALL, \
    LEFT_MOVE_JUMP, RIGHT_MOVE_JUMP, LEFT_MOVE_FALL, RIGHT_MOVE_FALL, \
    DEAD \
        = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14

    def __init__(self):
        self.x, self.y = 400, 130
        self.dir = 1
        self.total_frames = 0.0
        self.total_dead_frames = 0.0
        self.frame = 0
        self.dead_frame = 0
        self.state = self.RIGHT_STAND   # 플레이어 상태
        self.shot_state = False     # 샷 상태
        self.action_start_time = 0  # 점프, 슬라이딩 시작 시간
        self.shot_start_time = 0    # 샷 시작 시간
        self.accel = 1  # 가속
        self.left_key_state = False  # 좌측 키 누름 상태
        self.right_key_state = False # 우측 키 누름 상태
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
        Player.FALL_SPEED_KMPH -= 1  # Km / Hour
        Player.FALL_SPEED_MPM = (Player.FALL_SPEED_KMPH * 1000.0 / 60.0)
        Player.FALL_SPEED_MPS = (Player.FALL_SPEED_MPM / 60.0)
        Player.FALL_SPEED_PPS = (Player.FALL_SPEED_MPS * Player.PIXEL_PER_METER)
        distance = Player.FALL_SPEED_PPS * frame_time
        self.y += distance

        # 이동점프 중이면 x값을 변경
        if self.state in (self.LEFT_MOVE_JUMP, self.RIGHT_MOVE_JUMP):
            distance = Player.RUN_SPEED_PPS * frame_time
            self.x += (self.dir * distance)

        if get_time() - self.action_start_time > 0.3:  # 점프 시간이 0.x초를 지나면 낙하로 상태 변경
            Player.FALL_SPEED_KMPH = 80.0
            self.action_start_time = 0
            self.accel = 1
            if self.state in (self.LEFT_JUMP, ):
                self.state = self.LEFT_FALL
            elif self.state in (self.RIGHT_JUMP, ):
                self.state = self.RIGHT_FALL
            elif self.state in (self.LEFT_MOVE_JUMP, ):
                self.state = self.LEFT_MOVE_FALL
            elif self.state in (self.RIGHT_MOVE_JUMP, ):
                self.state = self.RIGHT_MOVE_FALL


    # 낙하
    def fall(self, frame_time):
        if self.y < 130 :
            self.y = 130
            if self.state in (self.LEFT_FALL, ):
                self.state = self.LEFT_STAND
            elif self.state in (self.RIGHT_FALL, ):
                self.state = self.RIGHT_STAND
            elif self.state in (self.LEFT_MOVE_FALL,):
                self.state = self.LEFT_RUN
            elif self.state in (self.RIGHT_MOVE_FALL,):
                self.state = self.RIGHT_RUN

        else:
            Player.FALL_SPEED_KMPH += 1  # Km / Hour
            Player.FALL_SPEED_MPM = (Player.FALL_SPEED_KMPH * 1000.0 / 60.0)
            Player.FALL_SPEED_MPS = (Player.FALL_SPEED_MPM / 60.0)
            Player.FALL_SPEED_PPS = (Player.FALL_SPEED_MPS * Player.PIXEL_PER_METER)
            distance = Player.FALL_SPEED_PPS * frame_time
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

        #self.dead_effect_ypos = self.dead_effect_ypos + distance


    def get_bb(self):
        return self.x - Player.STAND_BB_WIDTH, self.y - Player.STAND_BB_HEIGHT, self.x + Player.STAND_BB_WIDTH, self.y + Player.STAND_BB_HEIGHT

    def draw_bb(self):
        draw_rectangle(*self.get_bb())




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
            if self.state in (self.LEFT_SLIDING, self.RIGHT_SLIDING):
                pass
            else:
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

        # q키 입력 : 사망
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_q):
            self.state = self.DEAD
            for i in range(0, 8):
                self.dead_effect_xpos[i] = self.x
                self.dead_effect_ypos[i] = self.y
                self.dead_effect_xpos2[i] = self.x
                self.dead_effect_ypos2[i] = self.y
                self.dead_effect_degree[i] = 45 * i



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

        if self.shot_state == True:
            self.shot(frame_time)

        print("Change Time: %f, Total Frames: %d" %(get_time(), self.total_frames))

    def draw(self):

        if self.state == self.LEFT_STAND:
            if self.shot_state == False:
                self.player_image.clip_draw(0, 200, 40, 40, self.x, self.y, Player.CHAR_SIZE, Player.CHAR_SIZE)
            else:
                self.player_image.clip_draw(0, 120, 40, 40, self.x, self.y, Player.CHAR_SIZE, Player.CHAR_SIZE)
        elif self.state == self.RIGHT_STAND:
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

def handle_events(frame_time):
    global running
    global player
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            player.handle_event(event)

def get_frame_time():

    global current_time

    frame_time = get_time() - current_time
    current_time += frame_time
    return frame_time

def main():

    open_canvas(800, 700)
    global player
    global current_time

    player = Player()
    stage = Stage()

    global running
    running = True

    current_time = get_time()

    while running:
        frame_time = get_frame_time()
        handle_events(frame_time)
        player.update(frame_time)

        clear_canvas()
        stage.draw()
        player.draw()

        player.draw_bb()

        update_canvas()

        #delay(0.04)
    close_canvas()

if __name__ == '__main__':
    main()