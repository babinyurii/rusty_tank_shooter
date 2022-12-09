import arcade

import math
from constants import *
from support_functions import load_animation


class EnemyBullet(arcade.Sprite):
    """
   
    """

    def __init__(self, anim_obj):
        super().__init__()
        self.textures = None
        self.scale = SPRITE_SCALING
        #self.textures = []
        self.cur_texture = 0
        #texture = arcade.load_texture("./sprites/ufo_bullet.png")
        self.textures = load_animation(anim_type="enemy_projectiles", anim_obj=anim_obj)
        #self.textures.append(texture)

        self.texture = self.textures[0]
        self.texture_limit = (UPDATES_PER_FRAME * len(self.textures)) - 1
        
    def update_animation(self, delta_time: float = 1 / 60):
        
        # -1 so as not to go out of list range
        if self.cur_texture > self.texture_limit:
            self.cur_texture = 0
        frame = self.cur_texture // UPDATES_PER_FRAME
        self.texture = self.textures[frame]
        self.cur_texture += 1

        
        

       


