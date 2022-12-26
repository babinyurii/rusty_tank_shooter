import arcade
import math
from constants import *
import random
from enemy_bullet import EnemyBullet
from support_functions import load_animation


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MAIN_PATH_SPRITES = "../resources/sprites/"





class Enemy(arcade.Sprite):
    """
    This class represents the Enemy on our screen.
    """

    def __init__(self, enemy_bullet_list, enemy_type):
        super().__init__()

        self.enemy_bullet_list = enemy_bullet_list


        #self.textures = [] # we create this attr. it doesn't exist in Sprite class
        # otherwise we'll get list has not attribute exists
        self.textures = None
        self.hurt_textures = None
        self.cur_texture = 0
        self.cur_texture_hurt = 0
       
        ######################################
        # loading frames
        self.textures = load_animation(anim_type="enemies", anim_obj=enemy_type)
        self.texture = self.textures[0]
        self.texture_limit = (UPDATES_PER_FRAME * len(self.textures)) - 1
        
        self.hurt_textures = load_animation(anim_type="enemies", anim_obj=enemy_type + "_hurt")
        self.hurt_texture_limit = (UPDATES_PER_FRAME_HURT * len(self.hurt_textures)) - 1
    
        self.hurt = False
        self.hurt_counter  = 0
       
    
        self.center_x = None
        self.center_y = None
        self.position_list = None
        self.cur_position = None
        
        self.speed = None
        
        self.player_sprite = None
        
        self.time_since_last_dash = None
        self.time_between_dashes = None

        self.time_since_last_firing = None
        self.time_between_firing = None

        self.bullet_speed = None
        self.lives = None
        self.scale = SPRITE_SCALING


        self.x_limits = None
        self.y_limits = None
        
        ########################
        # sounds
        self.sounds = None
        
        
        ##########################
        # for direction calculation
        self.prev_coord_x = None
        self.next_coord_x = None
        self.prev_coord_y = None
        self.next_coord_y = None
        self.moves_right = False
        self.moves_left = False
        self.moves_up = False
        self.moves_down = False
        
        # call warmup to get rid of freeze at the first shot
        #self.warmup()
        
        # load sound which will be an attribute of the obj.
        # call arcade.play_sound(self.sound_name) to play it. see shoot_randomly method f.e.
        #self.laser_sound = arcade.load_sound("../resources/sounds/laser_shot.wav")

    ####################################
    # try to warmup
    # but mind this method
    # i seems it may cause troubles
    #def warmup(self):
    #    self.center_x = -100
    #    self.center_y = 100
    #    self.warmup_shoot()
        #self.center_x = self.position_list[0][0]
        #self.center_y = self.position_list[0][1] 
    # warmup method ends
    #############################################

    def get_prev_coords(self):
        self.prev_coord_x = self.center_x
        self.prev_coord_y = self.center_y
        
    def get_next_coords(self):
        self.next_coord_x = self.center_x
        self.next_coord_y = self.center_y
        
    def get_direction_along_x_and_y(self):
        
        if self.prev_coord_x - self.next_coord_x < 0:
            self.moves_right = True
            self.moves_left = False
            
        if self.prev_coord_x - self.next_coord_x > 0:
            self.moves_right = False
            self.moves_left = True
            
        if self.prev_coord_y - self.next_coord_y < 0:
            self.moves_up = True
            self.moves_down = False
            
        if self.prev_coord_y - self.next_coord_y > 0:
            self.moves_up = False
            self.moves_down = True
                
        
        

    
    def update_animation(self, delta_time: float = 1 / 60):
        
        # -1 so as not to go out of list range
        if not self.hurt:
            if self.cur_texture > self.texture_limit:
                self.cur_texture = 0
            frame = self.cur_texture // UPDATES_PER_FRAME
            self.texture = self.textures[frame]
            self.cur_texture += 1
        else:
            frame = self.cur_texture_hurt // UPDATES_PER_FRAME_HURT
            self.texture = self.hurt_textures[frame]
            self.cur_texture_hurt += 1
           
            if self.cur_texture_hurt > self.hurt_texture_limit:
                self.hurt = False
                self.cur_texture_hurt  = 0

       

    def follow_path_from_finding(self):
        """ Have a sprite follow a path """

        # Where are we
        start_x = self.center_x
        start_y = self.center_y

        # Where are we going
        dest_x = self.position_list[self.cur_position][0]
        dest_y = self.position_list[self.cur_position][1]

        # X and Y diff between the two
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y

        # Calculate angle to get there
        angle = math.atan2(y_diff, x_diff)

        # How far are we?
        distance = math.sqrt((self.center_x - dest_x) ** 2 + (self.center_y - dest_y) ** 2)

        # How fast should we go? If we are close to our destination,
        # lower our speed so we don't overshoot.
        speed = min(self.speed, distance)

        # Calculate vector to travel
        change_x = math.cos(angle) * speed
        change_y = math.sin(angle) * speed

        # Update our location
        self.center_x += change_x
        self.center_y += change_y  

        # How far are we?
        distance = math.sqrt((self.center_x - dest_x) ** 2 + (self.center_y - dest_y) ** 2)

        # If we are there, head to the next point.
        if distance <= self.speed:
            self.cur_position += 1

            # Reached the end of the list, start over.
            if self.cur_position >= len(self.position_list):
                self.cur_position = 0    

    def move_path(self):
        """ Have a sprite follow a path """

        # Where are we
        start_x = self.center_x
        start_y = self.center_y

        # Where are we going
        dest_x = self.position_list[self.cur_position][0]
        dest_y = self.position_list[self.cur_position][1]

        # X and Y diff between the two
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y

        # Calculate angle to get there
        angle = math.atan2(y_diff, x_diff)

        # How far are we?
        distance = math.sqrt((self.center_x - dest_x) ** 2 + (self.center_y - dest_y) ** 2)

        # How fast should we go? If we are close to our destination,
        # lower our speed so we don't overshoot.
        speed = min(self.speed, distance)

        # Calculate vector to travel
        change_x = math.cos(angle) * speed
        change_y = math.sin(angle) * speed

        # Update our location
        self.center_x += change_x
        self.center_y += change_y  

        # How far are we?
        distance = math.sqrt((self.center_x - dest_x) ** 2 + (self.center_y - dest_y) ** 2)

        # If we are there, head to the next point.
        if distance <= self.speed:
            self.cur_position += 1

            # Reached the end of the list, start over.
            if self.cur_position >= len(self.position_list):
                self.cur_position = 0


    def shoot_randomly(self, bullet_type, sound, delta_time: float = 1 / 60):
        # Loop through each enemy that we have
        
        # Have a random 1 in 200 change of shooting each 1/60th of a second
        odds = 200
        # Adjust odds based on delta-time
        adj_odds = int(odds * (1 / 60) / delta_time)
        if random.randrange(adj_odds) == 0:
            #arcade.play_sound(self.ufo_shot_sound)
            bullet = EnemyBullet(anim_obj=bullet_type)
            bullet.center_x = self.center_x
            #bullet.angle = -90
            bullet.top = self.bottom
            bullet.change_y = - ENEMY_BULLET_SPEED
            self.enemy_bullet_list.append(bullet)
            arcade.play_sound(sound, volume=0.5)
            
            ##################################
            # play sound which is the attribute of the object (see load sound at init)
            #arcade.play_sound(self.laser_sound)

    def enemy_bounce(self):
         #move the rectangle

        self.center_x += self.change_x
        self.center_y += self.change_y
        # check if we need to bounce of right edge
        if self.center_x > SCREEN_WIDTH - self.width / 2:
            self.change_x *= -1
        # check if we need to bounce of top edge
        if self.center_y > SCREEN_HEIGHT - self.height / 2:
            self.change_y *= -1
        # if we need to bounce of left edge # TODO smth's wrong. should be SCREEN_WIDHT
        #if self.center_x < self.width / 2:
        if self.left < 0:
            self.change_x *= -1
        # if we need to bounce of bottom edge # TODO the same as above 
        #if self.center_y < self.height / 2:
        if self.bottom < 0:
            self.change_y *= -1


    def warmup_shoot(self):
       
        #arcade.play_sound(self.ufo_shot_sound)
        bullet = EnemyBullet(anim_obj="horizontal_sentinel_bullet")
        bullet.center_x = self.center_x
        #bullet.angle = -90
        bullet.top = self.bottom
        bullet.change_y = - ENEMY_BULLET_SPEED
        self.enemy_bullet_list.append(bullet)




    
    def dash_to_a_point(self,  new_pos_x, new_pos_y, delta_time: float = 1 / 60):    
        
        
            
        # Where are we
        start_x = self.center_x
        start_y = self.center_y

        # Where are we going
        dest_x = new_pos_x
        dest_y = new_pos_y

        # X and Y diff between the two
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y

        # Calculate angle to get there
        angle = math.atan2(y_diff, x_diff)

        # How far are we?
        distance = math.sqrt((self.center_x - dest_x) ** 2 + (self.center_y - dest_y) ** 2)

        # How fast should we go? If we are close to our destination,
        # lower our speed so we don't overshoot.
        speed = min(self.speed, distance)

        # Calculate vector to travel
        change_x = math.cos(angle) * speed
        change_y = math.sin(angle) * speed

        # Update our location
        self.center_x += change_x
        self.center_y += change_y  

        # How far are we?
        distance = math.sqrt((self.center_x - dest_x) ** 2 + (self.center_y - dest_y) ** 2)

    def rush_to_a_single_point(self,  new_pos_x, new_pos_y, delta_time: float = 1 / 60):    
        
        
            
        # Where are we
        start_x = self.center_x
        start_y = self.center_y

        # Where are we going
        dest_x = new_pos_x
        dest_y = new_pos_y

        # X and Y diff between the two
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y

        # Calculate angle to get there
        angle = math.atan2(y_diff, x_diff)

        # How far are we?
        distance = math.sqrt((self.center_x - dest_x) ** 2 + (self.center_y - dest_y) ** 2)

        # How fast should we go? If we are close to our destination,
        # lower our speed so we don't overshoot.
        speed = min(self.speed, distance)

        # Calculate vector to travel
        change_x = math.cos(angle) * speed
        change_y = math.sin(angle) * speed

        # Update our location
        self.center_x += change_x
        self.center_y += change_y  

        # How far are we?
        distance = math.sqrt((self.center_x - dest_x) ** 2 + (self.center_y - dest_y) ** 2)
       
                
        # If we are there, head to the next point.
        if distance <= self.speed:
            self.on_attack = False
            #self.on_wait = True
                    
    def face_player(self):
        # Position the start at the enemy's current location
        start_x = self.center_x
        start_y = self.center_y

        # Get the destination location for the bullet
        dest_x = self.player.center_x
        dest_y = self.player.center_y

        # Do math to calculate how to get the bullet to the destination.
        # Calculation the angle in radians between the start points
        # and end points. This is the angle the bullet will travel.
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)

        ############################################
        ######################################3
        # Set the enemy to face the player.
        # + 90 was empirically addded. quick fix to make ufos 
        # face the player
        self.angle = math.degrees(angle) + 90

    
    def aim_and_shoot(self, bullet_type, delta_time: float = 1 / 60):
        # Loop through each enemy that we have
        
        
        # Position the start at the enemy's current location
        start_x = self.center_x
        start_y = self.center_y

        # Get the destination location for the bullet
        dest_x = self.player.center_x
        dest_y = self.player.center_y

        # Do math to calculate how to get the bullet to the destination.
        # Calculation the angle in radians between the start points
        # and end points. This is the angle the bullet will travel.
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)
        odds = 200
        
        # Adjust odds based on delta-time
        adj_odds = int(odds * (1 / 60) / delta_time)
        if random.randrange(adj_odds) == 0:
            bullet = EnemyBullet(anim_obj=bullet_type)
            bullet.center_x = self.center_x
            bullet.center_y = self.center_y
            # Angle the bullet sprite
            bullet.angle = math.degrees(angle)
            # Taking into account the angle, calculate our change_x
            # and change_y. Velocity is how fast the bullet travels.
            bullet.change_x = math.cos(angle) * ENEMY_BULLET_SPEED
            bullet.change_y = math.sin(angle) * ENEMY_BULLET_SPEED

            self.enemy_bullet_list.append(bullet)


    
    def shoot_periodically(self, bullet_type, delta_time: float = 1 / 60):
        """ Update this sprite. """

        # Track time since we last fired
        self.time_since_last_firing += delta_time

        # If we are past the firing time, then fire
        if self.time_since_last_firing >= self.time_between_firing:

            # Reset timer
            self.time_since_last_firing = 0

            # Fire the bullet
            bullet = EnemyBullet(anim_obj=bullet_type)
            bullet.center_x = self.center_x
            #bullet.angle = -90
            bullet.top = self.bottom
            bullet.change_y = - self.bullet_speed
            self.enemy_bullet_list.append(bullet)

    
    def shoot_on_command(self, bullet_type, delta_time: float = 1 / 60):
      

        # Fire the bullet
        bullet = EnemyBullet(anim_obj=bullet_type)
        bullet.center_x = self.center_x
        #bullet.angle = -90
        bullet.top = self.bottom
        bullet.change_y = -2
        self.enemy_bullet_list.append(bullet)


    
    
    def follow_sprite_on_distance(self):
        """
        This function will move the current sprite towards whatever
        other sprite is specified as a parameter.

        We use the 'min' function here to get the sprite to line up with
        the target sprite, and not jump around if the sprite is not off
        an exact multiple of SPRITE_SPEED.
        """

        self.center_x += self.change_x
        self.center_y += self.change_y

        # Random 1 in 100 chance that we'll change from our old direction and
        # then re-aim toward the player
        #if random.randrange(100) == 0:
        # UNCOMMENT IF WANT SOME RANDOM DIRECTIONS OF ENEMY
        start_x = self.center_x
        start_y = self.center_y

        # Get the destination location for the bullet
        dest_x = self.player.center_x
        dest_y = self.player.center_y

        # Do math to calculate how to get the bullet to the destination.
        # Calculation the angle in radians between the start points
        # and end points. This is the angle the bullet will travel.
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)

        # Taking into account the angle, calculate our change_x
        # and change_y. Velocity is how fast the bullet travels.
        self.change_x = math.cos(angle) * self.speed
        self.change_y = math.sin(angle) * self.speed

        distance = math.sqrt((self.center_x - dest_x) ** 2 + (self.center_y - dest_y) ** 2)

        if distance == 200: # here you can put attr which will be the limit of distance to player
            self.change_x = 0 # it seems better to init the attr at the init
            self.change_y = 0
        if self.center_y <= 200:
            self.change_y = 0
        if distance < 200:
            self.change_y += self.speed


    
    def follow_sprite(self):
        """
        This function will move the current sprite towards whatever
        other sprite is specified as a parameter.

        We use the 'min' function here to get the sprite to line up with
        the target sprite, and not jump around if the sprite is not off
        an exact multiple of SPRITE_SPEED.
        """

        self.center_x += self.change_x
        self.center_y += self.change_y

        # Random 1 in 100 chance that we'll change from our old direction and
        # then re-aim toward the player
        #if random.randrange(100) == 0:
        # UNCOMMENT IF WANT SOME RANDOM DIRECTIONS OF ENEMY
        start_x = self.center_x
        start_y = self.center_y

        # Get the destination location for the bullet
        dest_x = self.player.center_x
        dest_y = self.player.center_y

        # Do math to calculate how to get the bullet to the destination.
        # Calculation the angle in radians between the start points
        # and end points. This is the angle the bullet will travel.
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)

        # Taking into account the angle, calculate our change_x
        # and change_y. Velocity is how fast the bullet travels.
        self.change_x = math.cos(angle) * self.speed
        self.change_y = math.sin(angle) * self.speed
        
        
    
    def follow_path_from_finding(self):
        """ Have a sprite follow a path """

        # Where are we
        start_x = self.center_x
        start_y = self.center_y
        
        # Where are we going
        dest_x = self.position_list[self.cur_position][0]
        dest_y = self.position_list[self.cur_position][1]

        # X and Y diff between the two
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y

        # Calculate angle to get there
        angle = math.atan2(y_diff, x_diff)

        # How far are we?
        distance = math.sqrt((self.center_x - dest_x) ** 2 + (self.center_y - dest_y) ** 2)

        # How fast should we go? If we are close to our destination,
        # lower our speed so we don't overshoot.
        speed = min(self.speed, distance)

        # Calculate vector to travel
        change_x = math.cos(angle) * speed
        change_y = math.sin(angle) * speed

        # Update our location
        self.center_x += change_x
        self.center_y += change_y  

        # How far are we?
        distance = math.sqrt((self.center_x - dest_x) ** 2 + (self.center_y - dest_y) ** 2)

        # If we are there, head to the next point.
        if distance <= self.speed:
            self.cur_position += 1

            # Reached the end of the list, start over.
            if self.cur_position >= len(self.position_list):
                self.cur_position = 0

       



    



    
    


    

    
