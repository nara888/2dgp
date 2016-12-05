import random
import json
import os

from pico2d import *

import game_framework
import title_state

from player import Player
from background import Background
from brick import Jetman_Long_Brick
from enemy import *
from boss import *
from ui import *

name = "MainState"

player = None
background = None
brick = None
enemy = None
boss = None
hp_bar = None
boss_hp_bar = None
bullet_list = None
start_time = 0

def create_world():
    global player, bullet_list, background, brick, enemy, boss, hp_bar, boss_hp_bar, start_time

    background = Background()
    player = Player()
    #enemy = Mr_shiniri()
    #brick = Jetman_Long_Brick()
    boss = JetMan()
    hp_bar = Hp_Bar(player)
    boss_hp_bar = Boss_Hp_Bar(boss)
    bullet_list = player.get_bullet_list()

    start_time = get_time()

def destroy_world():
    global player, bullet_list, background, brick, enemy, boss, hp_bar

    del(player)
    #del(enemy)
    del(boss)
    del(background)
    del(hp_bar)
    del(boss_hp_bar)
    if bullet_list:
        del(bullet_list)
    #del(brick)


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
    wait_time = 1

    if get_time() - start_time > wait_time:
        background.music_start()

    player.update(frame_time)
    #enemy.update(frame_time)
    boss.update(frame_time, player)
    hp_bar.update(frame_time)
    boss_hp_bar.update(frame_time)

    for bullet in bullet_list:
        if collide(boss, bullet):
            bullet_list.remove(bullet)
            if boss.hit_check() == False:
                boss.damaged(frame_time)


def draw(frame_time):
    clear_canvas()
    background.draw()
    player.draw()
    boss.draw()
    #enemy.draw()
    #brick.draw()
    hp_bar.draw()
    boss_hp_bar.draw()

    player.draw_bb()
    boss.draw_bb()

    update_canvas()


def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True



