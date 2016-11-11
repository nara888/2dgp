import random
import json
import os

from pico2d import *

import game_framework
import title_state

from player import Player
from background import Background

name = "MainState"

player = None
background = None

def create_world():
    global player, background

    player = Player()
    background = Background()

def destroy_world():
    global player, background

    del(player)
    del(background)


def enter():
    game_framework.reset_time()
    create_world()


def exit():
    destroy_world()


def pause():
    pass


def resume():
    pass


def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            else:
                player.handle_event(event)

"""
def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True
"""

def update(frame_time):
    player.update(frame_time)


def draw(frame_time):
    clear_canvas()
    background.draw()
    player.draw()

    update_canvas()





