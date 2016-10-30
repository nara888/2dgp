import sys
sys.path.append('../LabsAll/Labs')

from pico2d import *

running = None
key_state = None

KEY_UP, KEY_RIGHT, KEY_LEFT, KEY_JUMP = 0, 1, 2, 3

class Stage:
    def __init__(self):
        self.image = load_image('stage.png')

    def draw(self):
        self.image.draw(400, 350, 800, 700)


class Player:
    image = None
    global state_switch

    LEFT_RUN, RIGHT_RUN, LEFT_STAND, RIGHT_STAND, LEFT_JUMP, RIGHT_JUMP = 0, 1, 2, 3, 4, 5

    def handle_left_run(self):
        self.x -= 5
        if key_state == KEY_RIGHT:
            self.state = self.RIGHT_RUN
        elif key_state == KEY_UP:
            self.state = self.LEFT_STAND
        elif key_state == KEY_JUMP:
            self.state = self.LEFT_JUMP

    def handle_left_stand(self):
        if key_state == KEY_LEFT:
            self.state = self.LEFT_RUN
        elif key_state == KEY_RIGHT:
            self.state = self.RIGHT_RUN
        elif key_state == KEY_JUMP:
            self.state = self.LEFT_JUMP

    def handle_right_run(self):
        self.x += 5
        if key_state == KEY_LEFT:
            self.state = self.LEFT_RUN
        elif key_state == KEY_UP:
            self.state = self.RIGHT_STAND
        elif key_state == KEY_JUMP:
            self.state = self.RIGHT_JUMP

    def handle_right_stand(self):
        if key_state == KEY_LEFT:
            self.state = self.LEFT_RUN
        elif key_state == KEY_RIGHT:
            self.state = self.RIGHT_RUN
        elif key_state == KEY_JUMP:
            self.state = self.RIGHT_JUMP

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


    def update(self):
        self.cnt += 1
        if self.cnt % 5 == 0:
            self.frame = (self.frame + 1) % 3
        self.handle_state[self.state](self)

    handle_state = {
        LEFT_RUN: handle_left_run,
        RIGHT_RUN: handle_right_run,
        LEFT_STAND: handle_left_stand,
        RIGHT_STAND: handle_right_stand,
        LEFT_JUMP: handle_left_jump,
        RIGHT_JUMP: handle_right_jump
    }

    def __init__(self):
        self.x, self.y = 400, 120
        self.cnt = 0
        self.jump_cnt = 0
        self.frame = 0
        self.run_frames = 0
        self.stand_frames = 0
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


def handle_events():
    global running
    global key_state
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_KEYUP:
            key_state = KEY_UP
        elif event.type == SDL_KEYDOWN and event.key == SDLK_RIGHT:
            key_state = KEY_RIGHT
        elif event.type == SDL_KEYDOWN and event.key == SDLK_LEFT:
            key_state = KEY_LEFT
        elif event.type == SDL_KEYDOWN and event.key == SDLK_x:
            key_state = KEY_JUMP

def main():

    open_canvas(800, 700)

    player = Player()
    stage = Stage()

    global running
    running = True

    while running:
        handle_events()

        player.update()

        clear_canvas()
        stage.draw()
        player.draw()

        update_canvas()

        delay(0.02)
    close_canvas()

if __name__ == '__main__':
    main()