from pico2d import *

class Brick:

    image = None;

    def __init__(self):
        self.x, self.y = 0, 0
        if Brick.image == None:
            pass

    def update(self, frame_time):
        pass

    def draw(self):
        self.image.draw(self.x, self.y)

    def get_bb(self):
        return self.x - 90, self.y - 20, self.x + 90, self.y + 20

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

class Jetman_Long_Brick(Brick):
    image = None

    def __init__(self):
        self.x, self.y = 400, 300
        if Jetman_Long_Brick.image == None:
            Jetman_Long_Brick.image = load_image('jetman_brick2.png')

    def update(self, frame_time):
        pass

    def draw(self):
        self.image.clip_draw(0, 0, 78, 15, self.x, self.y, 200, 50)

    def get_bb(self):
        return self.x - 90, self.y - 20, self.x + 90, self.y + 20

    def draw_bb(self):
        draw_rectangle(*self.get_bb())