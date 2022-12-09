import random
import os
import time
import arcade

from player import Player
from level_setup import LEVEL_SETUP

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_MOVEMENT_SPEED, TILE_SCALING, PLAYER_BULLET_SPEED,\
    SPRITE_SCALING, GRAVITY, SCREEN_TITLE

from enemy_types import EnemySentinelHorizontal, EnemyBouncer, EnemySentinelVertical, Ghost, EnemyBomber, \
    EnemyHammer, EnemyKamikadze, EnemySticker
    
from particle_types import GroundHitByEnemyBullet, EnemyHitByPlayer, PlayerHitByEnemy, GroundHitByEnemyBullet, EnemyExplosion, \
    EnemyExplosionOnSize

from particle_maker import explode_enemy, reverse_explode, add_trace_to_player_bullet, add_hover_trace_to_player_bullet, \
    explode_particles_in_circle_out, add_hover_rect_trace_to_player_bullet


######################################################3
# layers
LAYER_NAME_PLATFORMS = "walls"
LAYER_ENEMIES = "enemies"
LAYER_PLAYER = "player"
LAYER_ENEMY_BULLETS = "enemy_bullets"
LAYER_EXPLOSIONS = "explosions"
LAYER_PLAYER_BULLETS = "player_bullets"
LAYER_ENEMIES_WALLS_FREE = "enemies_walls_free"
LAYER_ENEMY_BULLETS_WALL_FREE = "enemy_bullets_wall_free"
LAYER_ENEMIES_BOMBERS = "enemies_bombers"
LAYER_ENEMIES_HEAVY = "enemies_heavy"
LAYER_ENEMIES_PATH = "enemies_path"
LAYER_ENEMIES_BOMBS = "enemies_bombs"
LAYER_REVERSE_EXPLOSIONS = "reverse_explosions"




            
class MenuView(arcade.View):
    """menu view"""
    def on_show_view(self):
        """ Called when switching to this view"""
        arcade.set_background_color(arcade.color.SMOKY_BLACK)

    def on_draw(self):
        """draw the menu"""
        self.clear()
        arcade.draw_text("PRESS ENTER TO START",
                            SCREEN_WIDTH /2, SCREEN_HEIGHT / 2, arcade.color.WHITE_SMOKE, 
                            font_size=20, anchor_x="center")

    def on_key_press(self, key, modifiers):
        """use mouse press to advance to the game view"""
        if key == arcade.key.ENTER: 
            game_view = Game()
            game_view.setup()
            self.window.show_view(game_view)

class PauseView(arcade.View):
    
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        
    def on_show_view(self):
        #arcade.set_background_color(arcade.color.ORANGE) # TODO backg. color remains the same orange after you rerurn to game
        pass
    
    def on_draw(self):
        self.clear()
        arcade.draw_text("PAUSED", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("PRESS ESC TO RETURN", SCREEN_WIDTH / 2,
                         SCREEN_HEIGHT / 2,
                         arcade.color.WHITE,
                         font_size=20,
                         anchor_x="center")
        arcade.draw_text("PRESS ENTER FOR STARTUP MENU", 
                         SCREEN_WIDTH / 2,
                         SCREEN_HEIGHT / 2 - 50,
                         arcade.color.WHITE,
                         font_size=20,
                         anchor_x="center")
        
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:    
            self.window.show_view(self.game_view)
        # reset the game
        elif key == arcade.key.ENTER:
            menu = MenuView()
            self.window.show_view(menu)
            
            
class GameOverView(arcade.View):
    """ Class to manage the game over view """
    def on_show_view(self):
        """ Called when switching to this view"""
        arcade.set_background_color(arcade.color.BLACK_OLIVE)

    def on_draw(self):
        """ Draw the game over view """
        self.clear()
        arcade.draw_text("Game Over. Press ESCAPE to start again", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.WHITE_SMOKE, 30, anchor_x="center")

    def on_key_press(self, key, _modifiers):
        """ If user hits escape, go back to the main menu view """
        if key == arcade.key.ESCAPE:
            menu_view = MenuView()
            self.window.show_view(menu_view)



class Game(arcade.View):
    
    def __init__(self):
        # mind the () after super. otherwise you'll get an error
        # TypeError: descriptor '__init__' of 'super' object needs an argument
        # our args are in main actually
        super().__init__()  
        # track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        #############################
        # player related
        self.player_sprite = None
        self.score = 0
        # scene obj to store sprites in it: no need for sprite lists directlyб scene will contain them
        self.scene = None
        self.physics_engine = None
        self.camera = None
        self.gui_camera = None
        self.background = None
        self.tile_map = None
        #############################
        # level related
        self.num_of_enemies = None
        self.enemy_types = []
        self.level = 0
        self.maps = None
        ################################
        # start and end level timers
        self.reverse_timer = -1
        self.level_completed = False
        self.end_level_reverse_timer = 4
        self.game_over_timer = 5
        self.game_over = False
        
        self.all_enemy_types = []
        
        self.sounds = {"player": None,
                       "enemy" : None
                       }
        # wave related attrs
        self.timer_to_next_wave = None
        self.num_waves = None
        self.num_enemies_in_wave = None
        # !!! for now use enemy_types var see above
        self.enemies_list = None
        self.timer_between_enemies = None
        self.enemy_in_wave_counter = 0
        self.level_setup = None
    
        
    
    
    def setup(self):
        
        self.all_enemy_types = [EnemySentinelHorizontal]
        # if self.width, self.height not used, will use window width and height
        self.camera = arcade.Camera()
        self.gui_camera = arcade.Camera()
        
        map_name = self.choose_map()
        print("=========================")
        print(map_name)
        # Layer specific options are defined based on Layer names in a dictionary
        # Doing this will make the SpriteList for the platforms layer
        # use spatial hashing for detection.
        layer_options = {"walls": {"use_spatial_hash": True,},}
        # Read in the tiled map
        #self.tile_map = arcade.load_tilemap(map_name, layer_options=layer_options)
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options=layer_options) # !!! here scaled!

        # Initialize Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        self.score = 0
        
        # loop starts
        self.scene.add_sprite_list(LAYER_ENEMY_BULLETS)
        self.scene.add_sprite_list(LAYER_ENEMIES)
        self.scene.add_sprite_list(LAYER_EXPLOSIONS)
        self.scene.add_sprite_list(LAYER_ENEMIES_WALLS_FREE)
        self.scene.add_sprite_list(LAYER_ENEMIES_BOMBERS) 
        self.scene.add_sprite_list(LAYER_ENEMIES_HEAVY) 
        self.scene.add_sprite_list(LAYER_ENEMIES_PATH)
        self.scene.add_sprite_list(LAYER_ENEMIES_BOMBS)
        self.scene.add_sprite_list(LAYER_REVERSE_EXPLOSIONS)
        # setup player
        self.scene.add_sprite_list(LAYER_PLAYER)
        self.scene.add_sprite_list(LAYER_PLAYER_BULLETS)
        # loop ends
        ########################################################
        self.player_sprite = Player(bullets=self.scene[LAYER_PLAYER_BULLETS])
        self.scene.add_sprite(LAYER_PLAYER, self.player_sprite)
        self.scene.add_sprite(LAYER_PLAYER, self.player_sprite.barrel)
        self.player_sprite.explosion_layer = self.scene[LAYER_EXPLOSIONS]
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             gravity_constant=GRAVITY,
                                                             walls=self.scene["walls"])
       
       
        #arcade.set_background_color(arcade.color.BLACK)
        # Set the background color
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)
       
        ############################3
        # sounds
        self.collect_sounds()
        self.warm_up_sounds()
        #print(self.sounds)
        self.player_sprite.sounds = self.sounds
        
        self.warm_up()
        
        self.add_player()
        self.center_camera_to_player()
        self.level_1()
    
    
    
    def make_new_map_and_layers(self):
        map_name = self.choose_map()
       
        # Layer specific options are defined based on Layer names in a dictionary
        # Doing this will make the SpriteList for the platforms layer
        # use spatial hashing for detection.
        layer_options = {"walls": {"use_spatial_hash": True,},} # !!! spatial hash for platforms
        # Read in the tiled map
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options=layer_options) # !!! here scaled!
        # Initialize Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
             
        # loop starts
        # TODO make layer addition in a for loop. put all names in array
        self.scene.add_sprite_list(LAYER_ENEMY_BULLETS)
        self.scene.add_sprite_list(LAYER_ENEMIES)
        self.scene.add_sprite_list(LAYER_EXPLOSIONS)
        self.scene.add_sprite_list(LAYER_ENEMIES_WALLS_FREE)
        self.scene.add_sprite_list(LAYER_ENEMIES_BOMBERS) 
        self.scene.add_sprite_list(LAYER_ENEMIES_HEAVY) 
        self.scene.add_sprite_list(LAYER_ENEMIES_PATH)
        self.scene.add_sprite_list(LAYER_ENEMIES_BOMBS)
        self.scene.add_sprite_list(LAYER_EXPLOSIONS)
        self.scene.add_sprite_list(LAYER_REVERSE_EXPLOSIONS)
        # setup player
        self.scene.add_sprite_list(LAYER_PLAYER)
        self.scene.add_sprite_list(LAYER_PLAYER_BULLETS) 
        # loop ends
        ######################################
        
        
        self.player_sprite.bullets=self.scene[LAYER_PLAYER_BULLETS] # !!! as the player add bullets, you should pass 
        self.scene.add_sprite(LAYER_PLAYER, self.player_sprite)    
        self.scene.add_sprite(LAYER_PLAYER, self.player_sprite.barrel)
        self.player_sprite.explosion_layer = self.scene[LAYER_EXPLOSIONS]
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             gravity_constant=GRAVITY,
                                                             walls=self.scene["walls"])
        
    def choose_map(self): 
        path = "../resources/maps/zone_1/"
        maps_list = os.listdir(path)
        maps_list = [x for x in maps_list if x.endswith("tmj")]
        
        return path + random.choice(maps_list)
   
        
    def collect_sounds(self):
        for key in self.sounds.keys():
            sounds_names = os.listdir(f"../resources/sounds/{key}/")
            self.sounds[key] = dict.fromkeys(sounds_names)
            for sound_name in self.sounds[key].keys():
                self.sounds[key][sound_name] = arcade.load_sound(f"../resources/sounds/{key}/{sound_name}")
                
                      
    def warm_up_sounds(self):
        for key in self.sounds.keys():
            for sound in self.sounds[key].keys():
                arcade.play_sound(self.sounds[key][sound], volume=0.0)
        
                
    def warm_up(self):
        
        for enemy_type in self.all_enemy_types:
           enemy = enemy_type(self.player_sprite, 
                              self.scene[LAYER_ENEMY_BULLETS])
           self.scene.add_sprite(LAYER_ENEMIES, enemy)
           
        for enemy in self.scene[LAYER_ENEMIES]:
            enemy.center_x = -100
            enemy.center_y = 100
            enemy.warmup_shoot()
        
        for enemy in self.scene[LAYER_ENEMIES]:
            enemy.remove_from_sprite_lists()
        
        for bullet in self.scene[LAYER_ENEMY_BULLETS]:
            bullet.remove_from_sprite_lists()
            
        self.player_sprite.center_x = -100
        self.player_sprite.warm_up_shoot()
        self.center_x = 200 ##TODO  remove after you make function place_the_player
        
         
        
    def add_enemies(self):
        # placing enemies without colliding with each other and walls
        for i in range(self.num_of_enemies): # number of enemies
            enemy_placed_successfully = False
            while not enemy_placed_successfully:
                # Position the enemy
                enemy_type = random.choice(self.enemy_types)
                enemy = enemy_type(self.player_sprite, self.scene[LAYER_ENEMY_BULLETS])
         
                wall_hit_list = arcade.check_for_collision_with_list(enemy, self.scene["walls"])
                enemy_hit_list = arcade.check_for_collision_with_list(enemy, self.scene["enemies"])
    
                if len(wall_hit_list) == 0 and len(enemy_hit_list) == 0:
                    enemy_placed_successfully = True
                    
                    # TODO
                    # here we put ordinary enemies, which are afraid of walls
                    # uncomment after ghosts and put into separate function
                    #self.scene.add_sprite(LAYER_ENEMIES_BOMBS, enemy)
                    enemy.sounds = self.sounds
                    self.scene.add_sprite(LAYER_ENEMIES, enemy)
                    
                    #self.scene.add_sprite(LAYER_ENEMIES_HEAVY, enemy) # TODO for hammer
                    #self.scene.add_sprite(LAYER_ENEMIES_WALLS_FREE, enemy)
           
                #enemy = EnemySentinelHorizontal(self.player_sprite, self.scene["enemy_bullets"],
                #                              self.scene["walls"])
                #self.scene.add_sprite("enemies", enemy)
        
    
    def add_player(self):
        
        placed_successfully = False
        while not placed_successfully:
            self.player_sprite.center_x = random.randint(200, 300)
            self.player_sprite.center_y = random.randint(100, 200)
            
            wall_hit_list = arcade.check_for_collision_with_list(self.player_sprite, 
                                                                 self.scene["walls"])
            enemy_hit_list = arcade.check_for_collision_with_list(self.player_sprite, 
                                                                  self.scene["enemies"])

            if len(wall_hit_list) == 0 and len(enemy_hit_list) == 0:
                placed_successfully = True
                self.player_sprite.barrel.position = self.player_sprite.position
                #self.player_sprite.sounds = self.sounds
                #self.scene.add_sprite(LAYER_PLAYER, self.player_sprite)
                
    def get_new_level_attrs(self):
        self.enemy_types = self.level_setup["enemies_list"]
        self.timer_to_next_wave = self.level_setup["timer_to_next_wave"]
        self.num_waves = self.level_setup["num_waves"]
        self.num_enemies_in_wave = self.level_setup["num_enemies_in_wave"]
        self.timer_between_enemies = self.level_setup["timer_between_enemies"]
        
        
    def level_1(self):
        #for key in self.tile_map.keys():
        #    print(key)
        self.reverse_timer = 6 #TODO fix for countdown on start
        self.level += 1
        self.level_setup = LEVEL_SETUP["level_1"]
        
        self.num_of_enemies = 5
        
        self.get_new_level_attrs()
        
        
        self.add_enemies()
        self.add_player()
    
        self.center_camera_to_player()
        
        
    def level_2(self):
        
        self.make_new_map_and_layers()
        self.level += 1
        self.level_setup = LEVEL_SETUP["level_2"]
        self.num_of_enemies = 10
        self.get_new_level_attrs()
        
        self.add_enemies()
        self.add_player()
        self.center_camera_to_player()
        
    def level_3(self):
        
        self.make_new_map_and_layers()
        self.level += 1
        self.level_setup = LEVEL_SETUP["level_3"]
        self.num_of_enemies = 10
        self.get_new_level_attrs()
        
        self.add_enemies()
        self.add_player()
        self.center_camera_to_player()
        
        
    def level_4(self):
        
        self.make_new_map_and_layers()
        self.level += 1
        self.level_setup = LEVEL_SETUP["level_4"]
        self.num_of_enemies = 10
        self.get_new_level_attrs()
        
        self.add_enemies()
        self.add_player()
        self.center_camera_to_player()
        
    def level_5(self):
        
        self.make_new_map_and_layers()
        self.level += 1
        self.level_setup = LEVEL_SETUP["level_5"]
        self.num_of_enemies = 10
        self.get_new_level_attrs()
        
        self.add_enemies()
        self.add_player()
        self.center_camera_to_player()
    
        
   
        
            
    def on_draw(self, delta_time:  float = 1 / 60):
        self.clear()
       
        # activate camera
        # !!! MIND THIS SEQUENCE:
        # 1. camera.use()
        # 2. scene.draw()
        # OTHERWISE IT WON'T MOVE
        self.camera.use()
        self.scene.draw()
        
        
        self.gui_camera.use()
        score_text = f"score: {self.score}"
        #draw score on the screen. scrolling with the viewport
        arcade.draw_text(score_text, 10, 10, arcade.color.WHITE, font_size=18)
        player_lives_text = f"lives: {self.player_sprite.lives}"
        arcade.draw_text(player_lives_text, 10, 30, arcade.color.WHITE, font_size=18)
        
        
        # first timer variant !!!
        #if self.timer_upto_moving < self.time_to_start_moving:
        
        if 0 <= self.reverse_timer < 4:
            
            arcade.draw_text(f"level {self.level} get ready", SCREEN_WIDTH / 2,
                             SCREEN_HEIGHT / 2, arcade.color.RED, font_size=50,
                             font_name="Kenney Blocks", anchor_x="center")
            countdown = int(self.reverse_timer)
            arcade.draw_text(f" {countdown} ", 
                             SCREEN_WIDTH / 2,
                             (SCREEN_HEIGHT / 2) - 50, 
                             arcade.color.RED, 
                             anchor_x="center",
                             font_size=50,
                             font_name="Kenney Blocks")
        
        elif 0 <= self.end_level_reverse_timer < 4:
            
            arcade.draw_text(f"level completed", SCREEN_WIDTH / 2,
                             SCREEN_HEIGHT / 2, arcade.color.RED, font_size=45,
                             font_name="Kenney Blocks", anchor_x="center")
            arcade.draw_text(f"get ready for the next", SCREEN_WIDTH / 2,
                             SCREEN_HEIGHT / 2 - 50, arcade.color.RED, font_size=45,
                             font_name="Kenney Blocks", anchor_x="center")
            countdown = int(self.end_level_reverse_timer)
            arcade.draw_text(f" {countdown} ", 
                             SCREEN_WIDTH / 2,
                             (SCREEN_HEIGHT / 2) - 100, 
                             arcade.color.RED, 
                             anchor_x="center",
                             font_size=50,
                             font_name="Kenney Blocks")
        elif self.game_over:
            arcade.draw_text("you lost...", SCREEN_WIDTH / 2,
                             SCREEN_HEIGHT / 2, arcade.color.RED, font_size=45,
                             font_name="Kenney Blocks", anchor_x="center")
            
            
    def make_new_enemy(self):
       
        #for i in range(self.num_enemies_in_wave): 
        enemy_placed_successfully = False
        while not enemy_placed_successfully:
           
            enemy_type = random.choice(self.enemy_types)
            enemy = enemy_type(self.player_sprite, self.scene[LAYER_ENEMY_BULLETS])
           
            wall_hit_list = arcade.check_for_collision_with_list(enemy, self.scene["walls"])

            # See if the enemy is hitting another enemy
            enemy_hit_list = arcade.check_for_collision_with_list(enemy, self.scene["enemies"])

            if len(wall_hit_list) == 0 and len(enemy_hit_list) == 0:
                
                enemy_placed_successfully = True
                enemy.sounds = self.sounds
                reverse_explode(enemy.center_x, enemy.center_y, self.scene[LAYER_REVERSE_EXPLOSIONS])
                arcade.play_sound(self.sounds["enemy"]["enemy_appears.wav"])
                self.scene.add_sprite(LAYER_ENEMIES, enemy)
                
        
    
    def on_update(self, delta_time:  float = 1 / 60):
        
        
        
        
        #self.scene[LAYER_PLAYER].update_animation() # TODO uncommend if animation in layer doesn't work
        
        ###############################################
        ##################################################
        # update animation !!!
        self.scene.update_animation(delta_time,[LAYER_PLAYER,  # TODO check if it's animated! 
                                                LAYER_ENEMIES,
                                                LAYER_ENEMY_BULLETS,
                                                LAYER_EXPLOSIONS,
                                                LAYER_PLAYER_BULLETS,
                                                LAYER_ENEMIES_WALLS_FREE,
                                                LAYER_ENEMIES_BOMBERS,
                                                LAYER_ENEMIES_HEAVY,
                                                LAYER_ENEMIES_PATH,
                                                LAYER_ENEMIES_BOMBS,
                                                LAYER_REVERSE_EXPLOSIONS])
        
        
           
       
        ##################################################
        
        

        
        #####################################################
        # !!! before update. as the coords will change after update
        #for enemy in self.scene[LAYER_ENEMIES]:
        #    enemy.get_prev_coords()
        
        ###################################
        #TODO can these timers slow the game?
        # may be it's better to put them in some kind of function
        # and make attr like self.objs_can_move
        # if self.objs_can_move:
        # the idea is: decrementing timer only when it's needed
        
        if self.reverse_timer >= 0:
            self.reverse_timer -= delta_time
       
        else:
            # collect current coords of the player
            self.player_sprite.prev_x = self.player_sprite.center_x
            self.player_sprite.prev_y = self.player_sprite.center_y
            # move player
            self.physics_engine.update()
            # collect new coords of the player
            self.player_sprite.next_x = self.player_sprite.center_x
            self.player_sprite.next_y = self.player_sprite.center_y
            #
            self.center_camera_to_player()
            # update all the stuff
            self.scene.update([LAYER_PLAYER,
                               LAYER_ENEMIES, 
                               LAYER_ENEMY_BULLETS,
                               LAYER_EXPLOSIONS,
                               LAYER_PLAYER_BULLETS,
                               LAYER_ENEMIES_WALLS_FREE,
                               LAYER_ENEMIES_HEAVY,
                               LAYER_ENEMIES_PATH,
                               LAYER_ENEMIES_BOMBS,
                               LAYER_REVERSE_EXPLOSIONS])
            
            ##################################################
            self.handle_enemy_bullets()
            self.handle_player_bullets()
            self.handle_enemies_bombs()   
            self.correct_enemies_clash_into_blocks_and_into_enemies()
        
            ######################
            # wave related
            ######################
            self.timer_to_next_wave -= delta_time
            if self.timer_to_next_wave < 0 and self.num_waves > 0:
                # timer between enemies
                self.timer_between_enemies -= delta_time
                if self.timer_between_enemies < 0:
                    self.timer_between_enemies = self.level_setup["timer_between_enemies"]
                    self.make_new_enemy()
                    self.num_enemies_in_wave -= 1
                    print("current num enemies in wave: ", self.num_enemies_in_wave)
                    #self.enemy_in_wave_counter += 1
                    # decrement num of enemies in a wave of some counter
                    # so that when all enemies placed
                    # update vars
                if self.num_enemies_in_wave == 0:
                    self.num_enemies_in_wave = self.level_setup["num_enemies_in_wave"]
                    self.timer_to_next_wave = self.level_setup["timer_to_next_wave"]
                    self.num_waves -= 1
                    print("timer to next wave: ", self.timer_to_next_wave)
                
                        
            if self.player_sprite.lives == 0 and not self.game_over:
                explosion_list = []
                explosion_list.append(self.player_sprite)
                self.player_sprite.remove_from_sprite_lists()
                explode_enemy(explosion_list, self.scene[LAYER_EXPLOSIONS])
                self.game_over = True
                
           
            if self.game_over:
                self.game_over_timer -= delta_time
                if self.game_over_timer < 0:
                    game_over_view = GameOverView()
                    self.window.show_view(game_over_view)
                    #self.timer_upto_moving = 0
                    self.reverse_timer = 4
            
            # TODO think of how to make next level switch a method so as not to repeat it
            if len(self.scene[LAYER_ENEMIES]) == 0 and self.level == 1 and self.num_waves == 0: # TODO just varian of level end condtion
                self.completed = True
                
                self.end_level_reverse_timer -= delta_time
                #print("end level timer: ", self.end_level_reverse_timer)
                if self.end_level_reverse_timer < 0:
                    self.completed = False
                    self.end_level_reverse_timer = 4
                    self.reverse_timer = 4
                    
                    self.level_2()
                    
                
            elif len(self.scene[LAYER_ENEMIES]) == 0 and self.level == 2 and self.num_waves == 0:
               self.completed = True
               
               self.end_level_reverse_timer -= delta_time
               if self.end_level_reverse_timer < 0:
                   self.completed = False
                   self.end_level_reverse_timer = 4
                   self.reverse_timer = 4
                   
                   self.level_3()
                
                
            elif len(self.scene[LAYER_ENEMIES]) == 0 and self.level == 3 and self.num_waves == 0:
                self.completed = True
                
                self.end_level_reverse_timer -= delta_time
                if self.end_level_reverse_timer < 0:
                    self.completed = False
                    self.end_level_reverse_timer = 4
                    self.reverse_timer = 4
                
                    self.level_4()
                
                
            elif len(self.scene[LAYER_ENEMIES]) == 0 and self.level == 4 and self.num_waves == 0:
                self.completed = True
                
                self.end_level_reverse_timer -= delta_time
                if self.end_level_reverse_timer < 0:
                    self.completed = False
                    self.end_level_reverse_timer = 4
                    self.reverse_timer = 4
               
                    self.level_5()
                
                
                
                
    def correct_enemies_clash_into_blocks_and_into_enemies(self):
        for enemy in self.scene[LAYER_ENEMIES]:
            #enemy.get_next_coords()
            #enemy.get_direction_along_x_and_y()
            
            hit_list_with_blocks = arcade.check_for_collision_with_list(enemy, 
                                                                        self.scene[LAYER_NAME_PLATFORMS])
            if hit_list_with_blocks:
                #print(len(hit_list_with_blocks))        
                
                #if enemy.moves_right and enemy.moves_up
                
              
                if enemy.moves_right:
                    enemy.change_x *= -1
                elif enemy.moves_left:
                    enemy.change_x *= -1
                
                if enemy.moves_up:
                    enemy.change_y *= -1
                elif enemy.moves_down:
                    enemy.change_y *= -1
                    
            
            hit_list_with_enemies = arcade.check_for_collision_with_list(enemy, 
                                                                        self.scene[LAYER_ENEMIES])
            if hit_list_with_enemies:
            
                if enemy.moves_right:
                    enemy.change_x *= -1
                elif enemy.moves_left:
                    enemy.change_x *= -1
                    
            
             # !!! TODO trying to have fun with player collision
            #hit_list_with_player = arcade.check_for_collision(enemy, self.player_sprite)
            #if hit_list_with_player:
                
            #    if enemy.moves_right:
            #         enemy.change_x *= -1
            #    elif enemy.moves_left:
            #         enemy.change_x *= -1  
            
    def handle_enemies_bombs(self):
        for enemy in self.scene[LAYER_ENEMIES_BOMBS]:
            hit_list = arcade.check_for_collision_with_list(enemy, self.scene[LAYER_NAME_PLATFORMS])
            if len(hit_list) > 0:
                
                enemy_exploded_list = []
                
                enemy.lives -= 1
                if enemy.lives == 0:
                    enemy_exploded_list.append(enemy)
                    #self.make_single_explosion(enemy, "player_hit_by_enemy")
                    enemy.remove_from_sprite_lists()
                    
                    ##########################################
                    # just put it here to hear the explosison
                    # TODO logic is not simple, so you have to put explosions here and there
                    #arcade.play_sound(self.enemy_explosion_sound)   
                    
                    self.make_explosion(enemy_exploded_list, "enemy_explosion",
                                    particle_count=10)  
        for enemy in self.scene[LAYER_ENEMIES_BOMBS]:
            hit_list = arcade.check_for_collision_with_list(enemy, self.scene[LAYER_PLAYER])
            if len(hit_list) > 0:
               
                enemy_exploded_list = []
                
                enemy.lives -= 1
                self.player_sprite.lives -= 1
                if enemy.lives == 0:
                    enemy_exploded_list.append(enemy)
                    #self.make_single_explosion(enemy, "player_hit_by_enemy")
                    enemy.remove_from_sprite_lists()
                    
                    ##########################################
                    # just put it here to hear the explosison
                    # TODO logic is not simple, so you have to put explosions here and there
                    #arcade.play_sound(self.enemy_explosion_sound)   
                    
                    self.make_explosion(enemy_exploded_list, "enemy_explosion",
                                    particle_count=10)    
        
            
            
    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""
        # first timer variant
        #if self.timer_upto_moving > self.time_to_start_moving:
        if self.reverse_timer < 0 and self.end_level_reverse_timer > 3:            
        #if self.reverse_timer > 0 or self.level_completed:
        #    pass
        #else:
            if key == arcade.key.SPACE:
                if self.physics_engine.can_jump():
                    #self.player_sprite.change_y = PLAYER_JUMP_SPEED
                    self.player_sprite.jump()
                    
            
            elif key == arcade.key.LEFT:
                self.left_pressed = True
                
                self.update_player_speed()
                
                
              
            elif key == arcade.key.RIGHT:
                self.right_pressed = True
                
                self.update_player_speed()
            
            if key == arcade.key.UP:
                #self.player_shoot()
                self.player_sprite.player_shoot()
                
                
            if key == arcade.key.ESCAPE:
                # pass self which is the current view to save this view state
                pause = PauseView(self)
                self.window.show_view(pause)
                
                
            if key == arcade.key.A:
                #self.player_sprite.barrel.rotate_around_point(self.player_sprite.position, 5)
                self.player_sprite.barrel.change_angle =  5
                                                             
            if key == arcade.key.S:
                #self.player_sprite.barrel.rotate_around_point(self.player_sprite.position,- 5)
                self.player_sprite.barrel.change_angle = - 5
                
           
                                                              
    
    def update_player_speed(self):
        self.player_sprite.change_x = 0
        #self.player_sprite.barrel.change_x = 0
        #self.player_sprite.change_y = 0
        
        
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = - PLAYER_MOVEMENT_SPEED
            #self.player_sprite.barrel.change_x = - PLAYER_MOVEMENT_SPEED
        if self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED     
            #self.player_sprite.barrel.change_x = PLAYER_MOVEMENT_SPEED
        
        

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key == arcade.key.LEFT:
            self.left_pressed = False
            self.update_player_speed()
       
        elif key == arcade.key.RIGHT:
            self.right_pressed = False
            self.update_player_speed()
       
        if key == arcade.key.A:
            self.player_sprite.barrel.change_angle = 0
        if key == arcade.key.S:
            self.player_sprite.barrel.change_angle = 0

    
    def center_camera_to_player(self):
        
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height / 2)
        
        # don't let camera travel past 0
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
            
        player_centered = screen_center_x, screen_center_y
        self.camera.move_to(player_centered)

   
    
   
     
    def handle_enemy_bullets(self, delta_time: float = 1 / 60):
        # Get rid of the bullet when it flies off-screen
        for bullet in self.scene[LAYER_ENEMY_BULLETS]:
            
            #if bullet.top < 0:
            #    bullet.remove_from_sprite_lists()
              # Check this bullet to see if it hit a coin
            hit_list = arcade.check_for_collision_with_list(bullet, self.scene[LAYER_PLAYER])
            # If it did...
            
            if len(hit_list) > 0:
                # Get rid of the bullet
                bullet.remove_from_sprite_lists()
                #explosion_maker = ExplosionMaker(hit_list, self.explosions_list)
                #self.make_explosion(hit_list, "player_hit_by_enemy") # TODO 
                self.player_sprite.lives -= 1
                arcade.play_sound(self.sounds["player"]["player_hurt.wav"])
                self.make_explosion(hit_list, "player_hit_by_enemy", particle_count=5)
              
                #self.player_sprite.being_hit = True
                
            
            bullet_hit_ground_list = []
            hit_ground_list = arcade.check_for_collision_with_list(bullet, 
                                                                   self.scene[LAYER_NAME_PLATFORMS])
            if hit_ground_list:
                bullet_hit_ground_list.append(bullet)
                self.make_explosion(bullet_hit_ground_list, "ground_hit_by_enemy_bullet",
                                    particle_count=5)
                bullet.remove_from_sprite_lists()
                #arcade.play_sound(self.bullet_hit_the_ground)
                
    def handle_player_bullets(self):
        # Loop through each bullet
        for bullet in self.scene[LAYER_PLAYER_BULLETS]:
            # Check this bullet to see if it hit a coin
            hit_list = arcade.check_for_collision_with_list(bullet, self.scene[LAYER_ENEMIES])
            # If it did...
            if len(hit_list) > 0:
                # Get rid of the bullet
                bullet.remove_from_sprite_lists()
                arcade.play_sound(self.sounds["enemy"]["enemy_hurt_1.wav"])
            #explosion_maker = ExplosionMaker(hit_list, self.explosions_list)
            self.make_explosion(hit_list, "enemy_hit_by_player", particle_count=5)

            enemy_exploded_list = []
            for enemy in hit_list:
                enemy.lives -= 1
                enemy.hurt = True
                if enemy.lives == 0:
                    #enemy.hurt = True #TODO try to make particle burst after the hurt animation ends
                    enemy_exploded_list.append(enemy)
                    explosion_sound_number = random.randint(1, 3)
                    explosion_sound_number = "enemy_explosion_" + str(explosion_sound_number) + ".wav"
                    arcade.play_sound(self.sounds["enemy"][explosion_sound_number])
                    #self.make_single_explosion(enemy, "player_hit_by_enemy")
                    enemy.remove_from_sprite_lists()
                    self.num_of_enemies -= 1
                    print("num of enemies: ", self.num_of_enemies)
                    self.score += 1
                    ##########################################
                    # just put it here to hear the explosison
                    # TODO logic is not simple, so you have to put explosions here and there
                    #arcade.play_sound(self.enemy_explosion_sound)   
                    
            #self.make_explosion(enemy_exploded_list, "enemy_explosion",
            #                    particle_count=10)
            explode_enemy(enemy_exploded_list, self.scene[LAYER_EXPLOSIONS])
            #explode_particles_in_circle_out(enemy_exploded_list, self.scene[LAYER_EXPLOSIONS])
        
        for bullet in self.scene[LAYER_PLAYER_BULLETS]:
            hit_list = arcade.check_for_collision_with_list(bullet, self.scene[LAYER_NAME_PLATFORMS])
            if len(hit_list) > 0:
                # Get rid of the bullet
                bullet.remove_from_sprite_lists()
            #explosion_maker = ExplosionMaker(hit_list, self.explosions_list)
            
            self.make_explosion(hit_list, "enemy_hit_by_player", particle_count=5) # TODO another type of explosion
            



    def make_explosion(self, hit_list, explosion_type, particle_count):
        for obj in hit_list:
            
            # Make an explosion
            for i in range(particle_count):
                if explosion_type == "ground_hit_by_enemy_bullet":
                    particle = GroundHitByEnemyBullet()
                    particle.center_x = obj.center_x
                    particle.center_y = obj.center_y
                    self.scene[LAYER_EXPLOSIONS].append(particle)
                #arcade.play_sound(self.enemy_explosion_sound)
                if explosion_type == "enemy_hit_by_player":
                    particle = EnemyHitByPlayer()
                    particle.position = obj.position
                    self.scene[LAYER_EXPLOSIONS].append(particle)
                if explosion_type == "player_hit_by_enemy":
                    particle = PlayerHitByEnemy()
                    particle.position = obj.position
                    self.scene[LAYER_EXPLOSIONS].append(particle)
                #if explosion_type == "enemy_explosion":
                #    particle = EnemyExplosion()
                #    particle.position = obj.position
                #    self.scene[LAYER_EXPLOSIONS].append(particle)
                #if explosion_type == "enemy_explosion":
                #    particle = EnemyExplosionOnSize()
                #    particle.position = obj.position
                #    self.scene[LAYER_EXPLOSIONS].append(particle)









def main():
    """ Startup """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()