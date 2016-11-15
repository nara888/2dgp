from pico2d import *

running = None

class Stage:
    def __init__(self):
        self.image = load_image('stage.png')

    def draw(self):
        self.image.draw(400, 350, 800, 700)

class Bullet:
    image = None

    PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
    BULLET_SPEED_KMPH = 60.0  # Km / Hour
    BULLET_SPEED_MPM = (BULLET_SPEED_KMPH * 1000.0 / 60.0)
    BULLET_SPEED_MPS = (BULLET_SPEED_MPM / 60.0)
    BULLET_SPEED_PPS = (BULLET_SPEED_MPS * PIXEL_PER_METER)

    def __init__(self):
        if Bullet.image == None:
            Bullet.image = load_image('resource/player/bullet.png')
        self.x, self.y = 200, 200
        self.bullet_size = 20
        self.dir = 1

    def move(self, frame_time):
        distance = Bullet.BULLET_SPEED_PPS * frame_time
        self.x += (self.dir * distance)

    def update(self, frame_time):
        self.move(frame_time)

    def draw(self):
        self.image.draw(self.x, self.y, self.bullet_size, self.bullet_size)


def get_frame_time():

    global current_time

    frame_time = get_time() - current_time
    current_time += frame_time
    return frame_time


def handle_events(frame_time):
    global running
    global bullet
    global bullet_list
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_z:
            if len(bullet_list) < 3:
                bullet_list.append(Bullet())

def main():

    open_canvas(800, 700)

    global bullet
    global current_time
    global running
    global bullet_list

    bullet_list = []
    running = True

    stage = Stage()

    current_time = get_time()

    while running:
        frame_time = get_frame_time()
        handle_events(frame_time)

        for bullet in bullet_list:
            bullet.update(frame_time)
            if bullet.x > 800 or bullet.x < 0:
                bullet_list.remove(bullet)

        clear_canvas()

        stage.draw()

        for bullet in bullet_list:
            bullet.draw()


        update_canvas()

    close_canvas()

if __name__ == '__main__':
    main()