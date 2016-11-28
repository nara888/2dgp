import random
import json
import os

from pico2d import *

import game_framework
import title_state

from player import Player
from player_bullet import Bullet
from background import Background
from brick import Jetman_Long_Brick
from enemy import *
from boss import *

name = "MainState"

player = None
player_bullet = None
background = None
brick = None
enemy = None
boss = None

def create_world():
    global player, bullet_list,  background, brick, enemy, boss

    background = Background()
    player = Player()
    #enemy = Mr_shiniri()
    #brick = Jetman_Long_Brick()
    boss = JetMan()
    bullet_list = []

def destroy_world():
    global player, bullet_list, background, brick, enemy, boss

    del(player)
    #del(enemy)
    del(boss)
    del(background)
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
                if (event.type, event.key) == (SDL_KEYDOWN, SDLK_z):
                    if player.state in (player.LEFT_SLIDING, player.RIGHT_SLIDING): # 플레이어가 슬라이딩 상태이면 블릿 생성 X
                        return
                    else:
                        if len(bullet_list) < 3:    # 블릿 리스트에 블릿이 2개 이하 이면 블릿 생성
                            bullet_list.append(Bullet(player))

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
    #enemy.update(frame_time)
    boss.update(frame_time, player)

    for bullet in bullet_list:
        bullet.update(frame_time)
        if bullet.x > 800 or bullet.x < 0:
            bullet_list.remove(bullet)


def draw(frame_time):
    clear_canvas()
    background.draw()
    player.draw()
    boss.draw()
    #enemy.draw()
    #brick.draw()
    for bullet in bullet_list:
        bullet.draw()

    update_canvas()





