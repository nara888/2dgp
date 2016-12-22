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
from sound_manager import *

name = "MainState"

player = None
background = None
brick = None
enemy = None
boss = None
hp_bar = None
boss_hp_bar = None
bullet_list = None
explosion_list = None
sound_manager = None
start_time = 0
clear_start_time = 0

clear_state = None

def create_world():
    global player, bullet_list, explosion_list, background, brick, enemy, boss, hp_bar, boss_hp_bar, sound_manager, start_time, clear_start_time, clear_state

    background = Background()
    sound_manager = Sound_Manager()
    player = Player()
    #enemy = Mr_shiniri()
    #brick = Jetman_Long_Brick()
    boss = JetMan()
    hp_bar = Hp_Bar(player)
    boss_hp_bar = Boss_Hp_Bar(boss)
    bullet_list = player.get_bullet_list()
    explosion_list = []

    clear_state = False

    player.set_sound_manager(sound_manager)
    boss.set_sound_manager(sound_manager)

    start_time = get_time()

def destroy_world():
    global player, bullet_list, background, brick, enemy, boss, hp_bar, boss_hp_bar, explosion_list, sound_manager

    del(player)
    #del(enemy)
    del(boss)
    del(background)
    del(hp_bar)
    del(boss_hp_bar)
    del(sound_manager)
    if bullet_list:
        del(bullet_list)
    if explosion_list:
        del(explosion_list)
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
                if clear_state == False:
                    player.handle_event(event)



def update(frame_time):
    global clear_state, start_time, music_start_time

    wait_time = 1

    end_trigger = False

    if get_time() - start_time > wait_time:
        sound_manager.battle_start()

    player.update(frame_time)
    #enemy.update(frame_time)
    boss.update(frame_time, player)
    hp_bar.update(frame_time)
    boss_hp_bar.update(frame_time)

    for exp in explosion_list:
        exp.update(frame_time)
        if exp.is_end_effect():
            explosion_list.remove(exp)

    for bullet in bullet_list:
        if collide(boss, bullet):
            bullet_list.remove(bullet)
            if boss.hit_check() == False:
                boss.damaged(frame_time)
                if boss.state == boss.dead:
                    sound_manager

    if collide(boss, player):
        if player.hit_check() == False and player.state != player.DEAD:
            player.damaged(frame_time, 5)

    if type(boss) == JetMan:
        if boss.jetman_missile:
            if collide(player, boss.jetman_missile):
                if player.hit_check() == False and player.state != player.DEAD:
                    player.damaged(frame_time, 3)
                explosion_list.append(Big_Explosion_Effect(boss.jetman_missile.x, boss.jetman_missile.y))
                boss.jetman_missile = None
                sound_manager.explosion()
            elif boss.jetman_missile.y < boss.jetman_missile.ground_y:
                explosion_list.append(Big_Explosion_Effect(boss.jetman_missile.x, boss.jetman_missile.y))
                boss.jetman_missile = None
                sound_manager.explosion()

        if boss.jetman_bomb_list:
            for bomb in boss.jetman_bomb_list:
                if collide(player, bomb):
                    if player.hit_check() == False and player.state != player.DEAD:
                        player.damaged(frame_time, 3)
                    explosion_list.append(Big_Explosion_Effect(bomb.x, bomb.y))
                    boss.jetman_bomb_list.remove(bomb)
                    sound_manager.explosion()
                elif bomb.y < bomb.ground_y:
                    explosion_list.append(Big_Explosion_Effect(bomb.x, bomb.y))
                    boss.jetman_bomb_list.remove(bomb)
                    sound_manager.explosion()

    for exp in explosion_list:
        if collide(player, exp):
            if player.hit_check() == False and player.state != player.DEAD and exp.is_end_damage():
                player.damaged(frame_time, 3)

    if boss.get_clear() and clear_state == False:
        clear_state = True
        player.get_clear_state()
        start_time = get_time()
        sound_manager.battle_end()

    if player.get_player_dead():
        sound_manager.battle_end()

    if clear_state and get_time() - start_time > 3:
        sound_manager.stage_clear()
        music_start_time = get_time()

    if player.get_end_state():
        game_framework.change_state(title_state)


def draw(frame_time):
    clear_canvas()
    background.draw()
    player.draw()
    boss.draw()
    #enemy.draw()
    #brick.draw()
    hp_bar.draw()
    boss_hp_bar.draw()

    for exp in explosion_list:
        exp.draw()

    #player.draw_bb()
    #boss.draw_bb()

    update_canvas()


def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True



