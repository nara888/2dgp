from pico2d import *

class Sound_Manager:

    battle_bgm = None
    clear_bgm = None
    shot_sound = None
    jump_sound = None
    damaged_sound = None
    enter_sound = None
    dead_sound = None
    out_sound = None

    regen_sound = None
    enem_damaged_sound = None
    missile_sound = None
    bomb_sound = None
    rock_on_sound = None
    landing_sound = None
    take_off_sound = None

    explosion_sound = None

    def __init__(self):
        if self.shot_sound == None:
            self.shot_sound = load_wav('resource/sound/shot.wav')
            self.shot_sound.set_volume(64)
        if self.jump_sound == None:
            self.jump_sound = load_wav('resource/sound/jump.wav')
            self.jump_sound.set_volume(64)
        if self.damaged_sound == None:
            self.damaged_sound = load_wav('resource/sound/damaged.wav')
            self.damaged_sound.set_volume(64)
        if self.enter_sound == None:
            self.enter_sound = load_wav('resource/sound/enter_stage.wav')
            self.enter_sound.set_volume(64)
        if self.out_sound == None:
            self.out_sound = load_wav('resource/sound/out_stage.wav')
            self.out_sound.set_volume(64)
        if self.dead_sound == None:
            self.dead_sound = load_wav('resource/sound/dead.wav')
            self.dead_sound.set_volume(64)
        if self.regen_sound == None:
            self.regen_sound = load_wav('resource/sound/regen.wav')
            self.regen_sound.set_volume(64)
        if self.enem_damaged_sound == None:
            self.enem_damaged_sound = load_wav('resource/sound/enem_damaged.wav')
            self.enem_damaged_sound.set_volume(64)
        if self.missile_sound == None:
            self.missile_sound = load_wav('resource/sound/missile.wav')
            self.missile_sound.set_volume(64)
        if self.bomb_sound == None:
            self.bomb_sound = load_wav('resource/sound/Bomb.wav')
            self.bomb_sound.set_volume(64)
        if self.rock_on_sound == None:
            self.rock_on_sound = load_wav('resource/sound/rock_on.wav')
            self.rock_on_sound.set_volume(64)
        if self.landing_sound == None:
            self.landing_sound = load_wav('resource/sound/landing.wav')
            self.landing_sound.set_volume(64)
        if self.take_off_sound == None:
            self.take_off_sound = load_wav('resource/sound/take_off.wav')
            self.take_off_sound.set_volume(64)

        if self.explosion_sound == None:
            self.explosion_sound = load_wav('resource/sound/explosion.wav')
            self.explosion_sound.set_volume(64)

    def battle_start(self):
        if self.battle_bgm == None:
            self.battle_bgm = load_music('resource/bgm/BossBattle.ogg')
            self.battle_bgm.set_volume(64)
            self.battle_bgm.repeat_play()

    def battle_end(self):
        self.battle_bgm.stop()

    def stage_clear(self):
        if self.clear_bgm == None:
            self.clear_bgm = load_music('resource/bgm/clear.ogg')
            self.clear_bgm.set_volume(64)
            self.clear_bgm.play()

    def shot(self):
        self.shot_sound.play()
    def jump(self):
        self.jump_sound.play()
    def damaged(self):
        self.damaged_sound.play()
    def enter_stage(self):
        self.enter_sound.play()
    def out_stage(self):
        self.out_sound.play()
    def dead(self):
        self.dead_sound.play()

    def regen(self):
        self.regen_sound.play(10)
    def enem_damaged(self):
        self.enem_damaged_sound.play()
    def missile(self):
        self.missile_sound.play()
    def bomb(self):
        self.bomb_sound.play()
    def rock_on(self):
        self.rock_on_sound.play()
    def landing(self):
        self.landing_sound.play()
    def take_off(self):
        self.take_off_sound.play()

    def explosion(self):
        self.explosion_sound.play()