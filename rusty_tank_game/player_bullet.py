import arcade
#from constants import *
import math
import os
from constants import *
from support_functions import load_animation
from particle_maker import add_hover_rect_trace_to_player_bullet
    
class PlayerBullet(arcade.Sprite):
    

    def __init__(self, particles):
        super().__init__()

        self.scale = 0.2
        self.textures = None
        
        self.textures = load_animation(anim_type="player_projectiles",
                                       anim_obj="player_bullet")
        
        
        self.texture = self.textures[0]
        self.texture_limit = (UPDATES_PER_FRAME * len(self.textures)) - 1
        self.cur_texture = 0
        self.layer_particles = particles
        
    def update_animation(self, delta_time: float = 1 / 60):
        
        # -1 so as not to go out of list range
        if self.cur_texture > self.texture_limit:
            self.cur_texture = 0
        frame = self.cur_texture // UPDATES_PER_FRAME
        self.texture = self.textures[frame]
        self.cur_texture += 1
        
    
    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        add_hover_rect_trace_to_player_bullet(self.center_x, self.bottom, 
                          self.layer_particles)
        
        if self.bottom > SCREEN_HEIGHT:
            self.remove_from_sprite_lists()

