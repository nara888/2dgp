from pico2d import *

import game_framework
import main_state

name = "TitleState"
image = None
bgm = None


def enter():
    global image, bgm
    image = load_image('resource/state/title.png')
    bgm = load_wav('resource/bgm/title.wav')
    bgm.set_volume(64)
    bgm.repeat_play()


def exit():
    global image, bgm
    del(image)
    del(bgm)


def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if(event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif(event.type, event.key) == (SDL_KEYDOWN, SDLK_RETURN):
                game_framework.change_state(main_state)


def draw(frame_time):
    global image

    clear_canvas()
    image.draw(400, 350)
    update_canvas()


def update(frame_time):
    pass

def pause():
    pass

def resume():
    pass






