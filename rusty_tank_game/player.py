import arcade
from constants import SPRITE_SCALING, UPDATES_PER_FRAME, PLAYER_MOVEMENT_SPEED, PLAYER_BULLET_SPEED
from support_functions import load_animation
from player_bullet import PlayerBullet
from particle_maker import player_shot_burst, reverse_explode
import math
PLAYER_JUMP_SPEED = 20


class RotatingSprite(arcade.Sprite):
    
    def rotate_around_point(self, point: arcade.Point, degrees: float):
        self.angle += degrees
        self.position = arcade.rotate_point(self.center_x, self.center_y,
                                            point[0], point[1],
                                            degrees)




class Player(arcade.Sprite):
    
    def __init__(self, bullets):
        super().__init__()
        
        self.scale = SPRITE_SCALING
        self.textures = None
        self.cur_texture = 0
        self.textures = load_animation(anim_type="player", anim_obj="player")
        self.textures_being_hit = load_animation(anim_type="player", anim_obj="player_being_hit")
        self.lives = 10
        
        self.texture = self.textures[0]
        self.texture_limit = (UPDATES_PER_FRAME * len(self.textures)) - 1
        
        self.center_x = 200
        self.center_y = 200
        
        self.bullet = None
        self.bullets = bullets
        self.time_between_shots = 0
        self.time_since_last_shot = 0
        self.can_shoot = True
        self.sounds = None
        self.explosion_layer = None
        # coords to get direction
        self.prev_x = None
        self.prev_y = None
        self.next_x = None
        self.next_y = None
        # movement direction
        self.moves_right = False
        self.moves_left = False
        self.moves_up = False
        self.moves_down = False
        
        ###############
        # barrel
        self.barrel = RotatingSprite("../resources/sprites/player/player_barrel/player_barrel.png", scale=SPRITE_SCALING)
        #self.barrel.center_x = self.center_x
        #self.barrel.center_y = self.center_y
        
    def get_direction(self):
        if (self.prev_x - self.next_x) < 0:
            self.moves_right = True
            self.moves_left = False
        elif (self.prev_x - self.next_x) > 0:
            self.moves_right = False
            self.moves_left = True
        else:
            pass
        
        if (self.prev_y - self.next_y) < 0:
            self.moves_up = True
            self.moves_down = False
        elif (self.prev_y - self.next_y) > 0:
            self.moves_up = False
            self.moves_down = True
        else:
            pass
            
        
    def update_animation(self, delta_time):
        #delta_time: float = 1 / 60        
        
        # -1 so as not to go out of list range
        if self.cur_texture > self.texture_limit:
            self.cur_texture = 0
        frame = self.cur_texture // UPDATES_PER_FRAME
        self.texture = self.textures[frame]
        #if self.being_hit:
        #    self.texture = self.textures_being_hit[frame]
        #    self.being_hit = False
        #else:
        #    self.texture = self.textures[frame]
            
        self.cur_texture += 1
    
    def update(self, delta_time = 1 / 60):
        """
        check left and right coords in
        movement and stay in the map
        
        """
        #print("left: ", self.left)
        #print("right: ", self.right)
        # check for out-of-bounds
        if self.left < 0:
            self.left = 0
        elif self.right > 1280:
            self.right = 1280
            
        if not self.can_shoot:
            self.time_since_last_shot += delta_time
            if self.time_since_last_shot > self.time_between_shots:
                self.time_since_last_shot = 0
                self.can_shoot = True
                
        self.get_direction()
        
        # move barrel with the body
        self.barrel.center_x = self.center_x
        self.barrel.center_y = self.center_y
        
        if self.barrel.angle > 100:
            self.barrel.angle = 100
        if self.barrel.angle < - 100:
            self.barrel.angle = - 100
        
        print("barrel angle: ", self.barrel.angle)
        #print("===============================")
        #print("moves_right: ", self.moves_right)
        #print("moves_left: ", self.moves_left)
        #print("moves_up: ", self.moves_up)
        #print("moves_down: ", self.moves_down)
                
    
            
    def jump(self):
        player_shot_burst(self.center_x, self.center_y, self.explosion_layer) # TODO make jump particles here
        self.change_y = PLAYER_JUMP_SPEED 
        arcade.play_sound(self.sounds["player"]["player_jump.wav"], volume=0.5)
       
        
        
    
    def player_shoot(self):
        if self.can_shoot:
            # Gunshot sound
            #arcade.play_sound(self.player_gun_sound)
            bullet = PlayerBullet(particles=self.explosion_layer)
            # Give the bullet a speed
            #bullet.change_y = PLAYER_BULLET_SPEED
            # Position the bullet
            bullet.center_x = self.center_x
            bullet.center_y = self.center_y
            # those calculations are taken from here
            # https://api.arcade.academy/en/latest/examples/sprite_rotate_around_tank.html#sprite-rotate-around-tank
            # see lines: 132, 133
            x_dir = math.cos(self.barrel.radians - math.pi / 2) * PLAYER_BULLET_SPEED
            y_dir = math.sin(self.barrel.radians - math.pi / 2) * PLAYER_BULLET_SPEED
            # minus in change_x and change_y sign is a quick fix. otherwise bullets go downwards
            bullet.change_x = - x_dir
            bullet.change_y = - y_dir
            
            arcade.play_sound(self.sounds["player"]["player_basic_shot.wav"], volume=0.5)
            # Add the bullet to the appropriate lists
            self.bullets.append(bullet)
            self.can_shoot = False
            player_shot_burst(self.center_x, self.top, self.explosion_layer)
            # handy test for particles, esp. reverse explosion
            #reverse_explode(self.center_x, self.top, self.explosion_layer)
            
            
    def warm_up_shoot(self):
        # Gunshot sound
        #arcade.play_sound(self.player_gun_sound)
        bullet = PlayerBullet(particles=self.explosion_layer)
        # Give the bullet a speed
        bullet.change_y = PLAYER_BULLET_SPEED
        # Position the bullet
        bullet.center_x = self.center_x
        bullet.bottom = self.top
        
        # Add the bullet to the appropriate lists
        self.bullets.append(bullet)
        
        
        
        
    
    
    
