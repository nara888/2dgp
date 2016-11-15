from pico2d import *


class Bullet:
    image = None

    PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
    BULLET_SPEED_KMPH = 90.0  # Km / Hour
    BULLET_SPEED_MPM = (BULLET_SPEED_KMPH * 1000.0 / 60.0)
    BULLET_SPEED_MPS = (BULLET_SPEED_MPM / 60.0)
    BULLET_SPEED_PPS = (BULLET_SPEED_MPS * PIXEL_PER_METER)

    BULLET_SIZE = 30

    def __init__(self, player):
        if Bullet.image == None:
            Bullet.image = load_image('resource/rockman/bullet.png')

        self.dir = player.dir
        self.y = player.y + 10

        if player.dir == 1:
            self.x = player.x + 40
        else:
            self.x = player.x - 40


    def move(self, frame_time):
        distance = Bullet.BULLET_SPEED_PPS * frame_time
        self.x += (self.dir * distance)

    def update(self, frame_time):
        self.move(frame_time)

    def draw(self):
        self.image.draw(self.x, self.y, Bullet.BULLET_SIZE, Bullet.BULLET_SIZE)