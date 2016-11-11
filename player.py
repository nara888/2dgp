import sys
sys.path.append('../LabsAll/Labs')

from pico2d import *

running = None


class Stage:
    def __init__(self):
        self.image = load_image('stage.png')

    def draw(self):
        self.image.draw(400, 350, 800, 700)


class Player:

    PIXEL_PER_METER = (10.0 / 0.3)              # 10 pixel 30 cm
    RUN_SPEED_KMPH = 20.0                       # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    SLIDING_SPEED_KMPH = 40.0  # Km / Hour
    SLIDING_SPEED_MPM = (SLIDING_SPEED_KMPH * 1000.0 / 60.0)
    SLIDING_SPEED_MPS = (SLIDING_SPEED_MPM / 60.0)
    SLIDING_SPEED_PPS = (SLIDING_SPEED_MPS * PIXEL_PER_METER)

    FALL_SPEED_KMPH = 40.0  # Km / Hour
    FALL_SPEED_MPM = (FALL_SPEED_KMPH * 1000.0 / 60.0)
    FALL_SPEED_MPS = (FALL_SPEED_MPM / 60.0)
    FALL_SPEED_PPS = (FALL_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    image = None

    LEFT_RUN, RIGHT_RUN, LEFT_STAND, RIGHT_STAND, LEFT_JUMP, RIGHT_JUMP, LEFT_SLIDING, RIGHT_SLIDING = 0, 1, 2, 3, 4, 5, 6, 7

    """
    def handle_left_jump(self):
        self.jump_cnt += 1
        if self.jump_cnt <= 15:
            self.y += 10
        elif self.jump_cnt > 15 and self.jump_cnt <= 30:
            self.y -= 10
        else:
            self.jump_cnt = 0
            self.state = self.LEFT_STAND

    def handle_right_jump(self):
        self.jump_cnt += 1
        if self.jump_cnt <= 15:
            self.y += 10
        elif self.jump_cnt > 15 and self.jump_cnt <= 30:
            self.y -= 10
        else:
            self.jump_cnt = 0
            self.state = self.RIGHT_STAND
    """
    # 이동
    def move(self, frame_time):
        distance = Player.RUN_SPEED_PPS * frame_time
        if self.state == self.RIGHT_RUN:
            self.dir = 1
            self.x += (self.dir * distance)



        elif self.state == self.LEFT_RUN:
            self.dir = -1
            self.x += (self.dir * distance)

    # 슬라이딩
    def sliding(self, frame_time):
        distance = Player.SLIDING_SPEED_PPS * frame_time
        if self.state == self.RIGHT_SLIDING:
            self.dir = 1
            self.x += (self.dir * distance)

        elif self.state == self.LEFT_SLIDING:
            self.dir = -1
            self.x += (self.dir * distance)

    # 낙하
    def fall(self, frame_time):
        if self.y < 130:
            return
        else:
            distance = Player.FALL_SPEED_PPS * frame_time
            self.y -= distance

    # 점프
    def jump(self):
        pass

    def handle_event(self, event):
        if(event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
            if self.state in (self.RIGHT_STAND, self.LEFT_STAND, self.RIGHT_RUN, self.LEFT_SLIDING, self.RIGHT_SLIDING):
                self.state = self.LEFT_RUN
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            if self.state in (self.RIGHT_STAND, self.LEFT_STAND, self.LEFT_RUN, self.LEFT_SLIDING, self.RIGHT_SLIDING):
                self.state = self.RIGHT_RUN
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_LEFT):
            if self.state in (self.LEFT_RUN, ):
                self.state = self.LEFT_STAND
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_RIGHT):
            if self.state in (self.RIGHT_RUN, ):
                self.state = self.RIGHT_STAND
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_x):
            if self.state in (self.RIGHT_STAND, self.RIGHT_RUN):
                self.state = self.RIGHT_JUMP
            elif self.state in (self.LEFT_STAND, self.LEFT_RUN):
                self.state = self.LEFT_JUMP
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_c):
            if self.state in (self.RIGHT_STAND, self.RIGHT_RUN):
                self.state = self.RIGHT_SLIDING
            elif self.state in (self.LEFT_STAND, self.LEFT_RUN):
                self.state = self.LEFT_SLIDING


    def update(self, frame_time):

        self.total_frames += Player.FRAMES_PER_ACTION * Player.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 3

        if self.state in (self.LEFT_RUN, self.RIGHT_RUN):
            self.move(frame_time)
        elif self.state in (self.LEFT_SLIDING, self.RIGHT_SLIDING):
            self.sliding(frame_time)

        self.fall(frame_time)

        print("Change Time: %f, Total Frames: %d" %(get_time(), self.total_frames))

    def __init__(self):
        self.x, self.y = 400, 400
        self.dir = 1
        self.total_frames = 0.0
        self.frame = 0
        self.char_size = 120
        self.state = self.RIGHT_STAND
        if Player.image == None:
            Player.image = load_image('player240x280.png')

    def draw(self):
        if(self.state == self.LEFT_STAND):
            self.image.clip_draw(0, 200, 40, 40, self.x, self.y, self.char_size, self.char_size)
        elif (self.state == self.RIGHT_STAND):
            self.image.clip_draw(0, 240, 40, 40, self.x, self.y, self.char_size, self.char_size)
        elif (self.state == self.LEFT_RUN):
            self.image.clip_draw(self.frame * 40 + 40, 200, 40, 40, self.x, self.y, self.char_size, self.char_size)
        elif (self.state == self.RIGHT_RUN):
            self.image.clip_draw(self.frame * 40 + 40, 240, 40, 40, self.x, self.y, self.char_size, self.char_size)
        elif self.state == self.LEFT_JUMP:
            self.image.clip_draw(160, 200, 40, 40, self.x, self.y, self.char_size, self.char_size)
        elif self.state == self.RIGHT_JUMP:
            self.image.clip_draw(160, 240, 40, 40, self.x, self.y, self.char_size, self.char_size)
        elif self.state == self.LEFT_SLIDING:
            self.image.clip_draw(200, 200, 40, 40, self.x, self.y, self.char_size, self.char_size)
        elif self.state == self.RIGHT_SLIDING:
            self.image.clip_draw(200, 240, 40, 40, self.x, self.y, self.char_size, self.char_size)

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

        update_canvas()

        delay(0.04)
    close_canvas()

if __name__ == '__main__':
    main()