# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 20:44:25 2022

@author: yuriy
"""

def on_key_press(self, key, modifiers):
    """called whenever a key is pressed"""

    #if key == arcade.key.UP:
    #    self.up_pressed = True
    #    self.update_player_speed()
    #elif key == arcade.key.DOWN:
    #    self.down_pressed = True
    #    self.update_player_speed()
    
  
    
    
    if key == arcade.key.SPACE:
        if self.physics_engine.can_jump():
            self.player_sprite.change_y = PLAYER_JUMP_SPEED
    
    if key == arcade.key.LEFT: # !!! was if before
        self.left_pressed = True
        self.update_player_speed()
    if key == arcade.key.RIGHT:
        self.right_pressed = True
        self.update_player_speed()

    #if key == arcade.key.UP:# Create a bullet
    #    self.player_shoot()
    #    arcade.play_sound(self.player_shot_sound )
        
    if key == arcade.key.ESCAPE:
        # pass self which is the current view to save this view state
        pause = PauseView(self)
        self.window.show_view(pause)



def on_key_release(self, key, modifiers):
    """callled when the user releases a key"""
    #if key == arcade.key.UP:
    #    self.up_pressed = False
    #    self.update_player_speed()
    #elif key == arcade.key.DOWN:
    #    self.down_pressed = False
    #    self.update_player_speed()
    if key == arcade.key.LEFT:
        self.left_pressed = False
        self.update_player_speed()
    elif key == arcade.key.RIGHT:
        self.right_pressed = False
        self.update_player_speed()



def update_player_speed(self):
    self.player_sprite.change_x = 0
    self.player_sprite.change_y = 0

    #if self.up_pressed and not self.down_pressed:
    #    self.player_sprite.change_y = MOVEMENT_SPEED
    #elif self.down_pressed and not self.up_pressed:
    #    self.player_sprite.change_y = - MOVEMENT_SPEED
    if self.left_pressed and not self.right_pressed:
        self.player_sprite.change_x = - PLAYER_MOVEMENT_SPEED
    elif self.right_pressed and not self.left_pressed:
        self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
    # quick fix for diagonal movement speed
    # a kind of normalizing for 45 degree move
    #  https://blenderartists.org/t/diagonal-movement-speed/455367
    #if self.up_pressed and self.left_pressed:
    #    self.player_sprite.change_x = - MOVEMENT_SPEED * 0.707
    #    self.player_sprite.change_y = MOVEMENT_SPEED * 0.707
    #if self.up_pressed and self.right_pressed:
    #    self.player_sprite.change_x = MOVEMENT_SPEED * 0.707
    #    self.player_sprite.change_y = MOVEMENT_SPEED * 0.707
    #if self.down_pressed and self.left_pressed:
    #    self.player_sprite.change_x = - MOVEMENT_SPEED * 0.707
    #    self.player_sprite.change_y = - MOVEMENT_SPEED * 0.707
    #if self.down_pressed and self.right_pressed:
    #    self.player_sprite.change_x = MOVEMENT_SPEED * 0.707
    #    self.player_sprite.change_y = - MOVEMENT_SPEED * 0.707
    
    
    
    
  def make_random_position(self):
      
      
      
      enemy_placed_successfully = False
     

      # Keep trying until success
      while not enemy_placed_successfully:
          new_pos_x = random.randint(self.x_lim[0], self.x_lim[1])
          new_pos_y = random.randint(self.y_lim[0], self.y_lim[1]) 
          
          x_pos_to_check = [new_pos_x, new_pos_x + 100, new_pos_x - 100]
          y_pos_to_check = [new_pos_y, new_pos_y + 100, new_pos_y - 100]
          
          colliding_walls = 0
          #colliding_enemies = 0
          
          for wall in self.walls:
              for x_pos in x_pos_to_check:
                  print(x_pos)
                 
                  if wall.collides_with_point((x_pos, new_pos_y)):
                      colliding_walls += 1
                     
                      
              for y_pos in y_pos_to_check:
                  
                  if wall.collides_with_point((new_pos_x, y_pos)):
                      colliding_walls += 1
                      
                  
          #for enemy in self.enemies:
          #    for y_pos in y_pos_to_check:
          #        if enemy.collides_with_point((new_pos_x, y_pos)):
          #            colliding_enemies += 1
          
              
              if  colliding_walls == 0:
                  enemy_placed_successfully = True
                  self.new_pos_x = new_pos_x
                  self.new_pos_y = new_pos_y
   ####################################################################3
############################################################################
# quick fix for ghost not to run into walls
###################################3
    # placing enemies without colliding with each other and walls
    for enemy in self.scene[LAYER_NAME_ENEMIES_WALLS_FREE]: # number of enemies
        # Boolean variable if we successfully placed the enemy
        enemy_placed_successfully = False
        enemy_old_center_x = enemy.center_x
        enemy_old_center_y = enemy.center_y
        # Keep trying until success
        while not enemy_placed_successfully:
            ###################################################################################
            # Position the enemy
            #enemy = EnemySentinelHorizontal(self.player_sprite, self.scene["enemy_bullets"])
            #enemy = EnemyBouncer(self.player_sprite, self.scene["enemy_bullets"])
            #enemy = EnemySentinelVertical(self.player_sprite, self.scene["enemy_bullets"])
            ###################################################################################
            new_pos_x = random.randint(enemy.x_lim[0], enemy.x_lim[1])
            new_pos_y = random.randint(enemy.y_lim[0], enemy.y_lim[1])
            # See if the coin is hitting a wall
            enemy.center_x = new_pos_x
            enemy.center_y = new_pos_y
            wall_hit_list = arcade.check_for_collision_with_list(enemy, self.scene["platforms"])
    
            # See if the enemy is hitting another enemy
            enemy_hit_list = arcade.check_for_collision_with_list(enemy, self.scene["enemies"])
    
            if len(wall_hit_list) == 0 and len(enemy_hit_list) == 0:
                # It is!
              
                enemy_placed_successfully = True
                
                # TODO
                # here we put ordinary enemies, which are afraid of walls
                # uncomment after ghots and put into separate function
                #self.scene.add_sprite("enemies", enemy)
                enemy.new_pos_x = new_pos_x
                enemy.new_pos_y = new_pos_y
                enemy.center_x = enemy_old_center_x
                enemy.center_y = enemy_old_center_y
       
          
    ########################################  
# --- Manage Scrolling ---
# Keep track of if we changed the boundary. We don't want to call the
# set_viewport command if we didn't change the view port.
changed = False

# Scroll left
left_boundary = self.view_left + VIEWPORT_MARGIN
if self.player_sprite.left < left_boundary:
    self.view_left -= left_boundary - self.player_sprite.left
    changed = True

# Scroll right
right_boundary = self.view_left + SCREEN_WIDTH - VIEWPORT_MARGIN
if self.player_sprite.right > right_boundary:
    self.view_left += self.player_sprite.right - right_boundary
    changed = True

# Scroll up
top_boundary = self.view_bottom + SCREEN_HEIGHT - VIEWPORT_MARGIN
if self.player_sprite.top > top_boundary:
    self.view_bottom += self.player_sprite.top - top_boundary
    changed = True

# Scroll down
bottom_boundary = self.view_bottom + VIEWPORT_MARGIN
if self.player_sprite.bottom < bottom_boundary:
    self.view_bottom -= bottom_boundary - self.player_sprite.bottom
    changed = True

# Make sure our boundaries are integer values. While the view port does
# support floating point numbers, for this application we want every pixel
# in the view port to map directly onto a pixel on the screen. We don't want
# any rounding errors.
self.view_left = int(self.view_left)
self.view_bottom = int(self.view_bottom)

# If we changed the boundary values, update the view port to match
if changed:
    arcade.set_viewport(self.view_left,
                        SCREEN_WIDTH + self.view_left,
                        self.view_bottom,
                        SCREEN_HEIGHT + self.view_bottom)
########################################################################
    

# old enemy inits

       #enemy = EnemyBouncer(self.player_sprite, self.scene["enemy_bullets"])
       #enemy = EnemySentinelVertical(self.player_sprite, self.scene["enemy_bullets"])
       #enemy = EnemyBomber(player=self.player_sprite, 
       #              enemy_bullet_list=self.scene[LAYER_ENEMY_BULLETS], 
       #              walls = self.scene["platforms"],
       #              enemies = self.scene[LAYER_ENEMIES_BOMBERS]) 
       #enemy = EnemyHammer(player=self.player_sprite, 
       #              enemy_bullet_list=self.scene[LAYER_ENEMY_BULLETS],
       #              walls=self.scene[LAYER_NAME_PLATFORMS]) # TODO: make constant names
       ###################################################################################
       #enemy = EnemyKamikadze(player=self.player_sprite, 
       #              enemy_bullet_list=self.scene[LAYER_ENEMY_BULLETS],
       #              walls=self.scene[LAYER_NAME_PLATFORMS]) # TODO: make constant names
       # See if the coin is hitting a wall
       
       #enemy = EnemySticker(player=self.player_sprite, enemy_bullet_list=self.scene[LAYER_ENEMY_BULLETS])
    