
import arcade
from constants import *
import random
from enemy import Enemy




SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
# you can put textures as constants here
# or you can put them into a separate file

 

class EnemySentinelHorizontal(Enemy):

    def __init__(self, player, enemy_bullet_list) :
    #def __init__(self, player, enemy_bullet_list, texture= MAIN_PATH_SPRITES + "horizontal_sentinel/sentinel_1.png"):
    #def __init__(self, player, enemy_bullet_list, texture=":resources:galaga_like/sprites/horizontal_sentinel/sentinel_1.png"):
        
        super().__init__(enemy_bullet_list=enemy_bullet_list, 
                        enemy_type="horizontal_sentinel")

        self.x_lim = [100, 1280] # TODO now it's the width of the first zone maps. should be set at every map game loads
        self.y_lim = [150, 600] 
        
      
        self.center_x = random.randint(self.x_lim[0], self.x_lim[1])
        self.center_y = random.randint(self.y_lim[0], self.y_lim[1])
            
  
        
        #self.position_list = [[50, self.center_y], [1500, self.center_y]]
        #self.center_x = 50
        #self.center_y = 400
        #self.cur_position = 0
        self.speed = 3
        self.lives = 3
        
        self.bullet = "horizontal_sentinel_bullet"   
        
        # where to go
        self.direction_left_or_right = random.choice([-1, 1])
        self.change_x = self.speed * self.direction_left_or_right
        

    def update(self, delta_time: float = 1 / 60):
       #self.move_path()
       self.get_prev_coords()
       self.move_horizontally()
       self.get_next_coords()
       self.get_direction_along_x_and_y()
       self.shoot_randomly(bullet_type=self.bullet, sound=self.sounds["enemy"]["enemy_horizontal_sentinel_shot.wav"])
       
       
       
    def move_horizontally(self):
        #print("enemy left: ", self.left)
        #print("enemy direction: ", self.direction_left_or_right)
        if self.left < 0:
            self.change_x *= -1
        elif self.right > 1650:
            self.change_x *= -1
        
        self.center_x += self.change_x
    
    
            

class EnemySentinelVertical(Enemy):

    def __init__(self, player, enemy_bullet_list):

        super().__init__(enemy_bullet_list=enemy_bullet_list, 
                        enemy_type="vertical_sentinel")
        
        self.x_lim = [100, 1650] # TODO : 
        self.y_lim = [150, 600] 
        self.center_x = random.randint(self.x_lim[0], self.x_lim[1])
        self.center_y = random.randint(self.y_lim[0], self.y_lim[1])
        self.cur_position = 0
        self.speed = 2
        self.lives = 3
        # where to go
        self.direction_up_or_down = random.choice([-1, 1])
        self.change_y = self.speed * self.direction_up_or_down
        
        self.bullet = "vertical_sentinel_bullet"
        
        
    def update(self, delta_time: float = 1 / 60):
       
       self.get_prev_coords()
       self.move_vertically()
       self.get_next_coords()
       self.get_direction_along_x_and_y()
       self.shoot_randomly(bullet_type=self.bullet, sound=self.sounds["enemy"]["enemy_horizontal_sentinel_shot.wav"])
       
    
    def move_vertically(self):
        #print("enemy left: ", self.left)
        #print("enemy direction: ", self.direction_left_or_right)
        if self.top > 650:
            self.change_y *= -1
        elif self.bottom < 0:
            self.change_y *= -1
        
        self.center_y += self.change_y
                


class EnemyBouncer(Enemy):

    def __init__(self, player, enemy_bullet_list):

        
        
        super().__init__(enemy_bullet_list=enemy_bullet_list, 
                        enemy_type="bouncer")

        self.x_lim = [100, 1650] # TODO : 
        self.y_lim = [150, 600] 
        
      
        self.center_x = random.randint(self.x_lim[0], self.x_lim[1])
        self.center_y = random.randint(self.y_lim[0], self.y_lim[1])
        
        # choose speed
        enemy_change_x = random.randint(1, 5)
        enemy_change_y = random.randint(1, 5)

        self.change_x = enemy_change_x
        self.change_y = enemy_change_y
        #self.center_x = enemy_start_x_pos
        #self.center_y = enemy_start_y_pos
        self.cur_position = 0
        self.speed = 10
        self.lives = 3
        self.bullet = "vertical_sentinel_bullet"
    
    def update(self, delta_time: float = 1 / 60):
       self.enemy_bounce()
       self.shoot_randomly(bullet_type=self.bullet)
       
       
       

        

class Ghost(Enemy):

    def __init__(self, enemy_bullet_list, player, walls, enemies):
                    
       
        super().__init__(enemy_bullet_list=enemy_bullet_list, 
                        enemy_type="ghost")


        self.x_lim = [100, 1650] # TODO : 
        self.y_lim = [150, 600] 
        
        #self.textures = [] # we create this attr. it doesn't exist in Sprite class
        # otherwise we'll get list has not attribute exists
        
        self.center_x = random.randint(self.x_lim[0], self.x_lim[1])
        self.center_y = random.randint(self.y_lim[0], self.y_lim[1]) 
        self.position_list = [[self.center_x, self.center_y]]

        self.cur_position = 0
        self.speed = 200
        self.time_since_last_dash = 0.0
        self.time_between_dashes = 3.0  # this can be contolled by access in different levels : faster and faser f.e.
         
        #self.make_random_positon_list()

        self.player = player
        self.lives = 3
        self.bullet = "ghost_bullet"
        self.walls = walls
        
        self.new_pos_x = None
        self.new_pos_y = None
        self.enemies = enemies
    
    #def make_random_positon_list(self):
        
    #    for i in range(100):
    #        x_pos = random.randint(self.x_lim[0], self.x_lim[1])
    #        y_pos = random.randint(self.y_lim[0], self.y_lim[1]) 
    #        self.position_list.append([x_pos, y_pos])
    
    def make_random_position(self):
        
        
        
       
        new_pos_x = random.randint(self.x_lim[0], self.x_lim[1])
        new_pos_y = random.randint(self.y_lim[0], self.y_lim[1]) 
       
        self.new_pos_x = new_pos_x
        self.new_pos_y = new_pos_y
              
                        
                
                
                    

            

            
                
              
                
        # check if position not inside the block
        
        
    

    def update(self, delta_time: float = 1 / 60):
        
        
        self.face_player()
        
        if arcade.has_line_of_sight(self.player.position,
                                            self.position,
                                            self.walls):
           
               
        
            self.aim_and_shoot(bullet_type=self.bullet)
                
        self.time_since_last_dash += delta_time
        if self.time_since_last_dash > self.time_between_dashes:
            self.make_random_position()
            
            self.dash_to_a_point(new_pos_x=self.new_pos_x,
                                 new_pos_y=self.new_pos_y)
            self.time_since_last_dash = 0
            
            

class EnemyBomber(Enemy):


    def __init__(self, enemy_bullet_list, player, walls, enemies):
                    
       
        super().__init__(enemy_bullet_list=enemy_bullet_list, 
                        enemy_type="bomber")
        
        self.x_lim = [100, 1650] # TODO : 
        self.y_lim = [200, 600] 
        self.center_x = random.randint(self.x_lim[0], self.x_lim[1])
        self.center_y = random.randint(self.y_lim[0], self.y_lim[1]) 
        self.player = player
        self.horizontal_speed = 1
     
        self.hovering_height = self.center_y
     
        
        self.on_search = True
        self.on_attack = False
        
        self.time_since_last_firing = 0
        self.time_between_firing = 0.5

        self.bullet_speed = 10
        self.lives = 3
        self.bullet = "bomber_bomb"
        
        self.enemies = enemies
        self.walls = walls

    def move_onto_player(self):
        
        
        if arcade.has_line_of_sight(self.player.position,
                                            self.position,
                                            self.walls):
           
            # should be all 'ifs' otherwise it freezes
            if self.center_x < self.player.center_x:
                self.center_x += self.horizontal_speed
            if self.center_x > self.player.center_x:
                self.center_x -= self.horizontal_speed
            if self.player.center_x - 10 <= self.center_x <= self.player.center_x + 10:
                self.on_search = False
                self.on_attack = True


    def update(self, delta_time: float = 1 / 60):
        
        
        
        if self.on_search:
            self.move_onto_player()
        elif self.on_attack:
            self.shoot_periodically(bullet_type=self.bullet)
            self.on_search = True
            self.on_attack = False
            
            

class EnemyHammer(Enemy):

    def __init__(self, enemy_bullet_list, player, walls):
                    
       
        super().__init__(enemy_bullet_list=enemy_bullet_list, 
                        enemy_type="hammer")
    
        self.x_lim = [50, 750]
        self.y_lim = [400, 550] 
        self.center_x = random.randint(self.x_lim[0], self.x_lim[1])
        self.center_y = random.randint(self.y_lim[0], self.y_lim[1]) 

        self.player = player
        self.horizontal_speed = 2
        self.hammering_speed = 10
        self.rising_speed = 5
        self.hovering_height = random.randint(self.y_lim[0], self.y_lim[1]) 

        
        self.on_search = True
        self.on_attack = False
        self.on_rise = False
        self.lives = 3
        
        self.walls = walls
    
    def move_onto_player(self):
        
        # should be all if's otherwise it freezes
        if self.center_x < self.player.center_x:
            self.center_x += self.horizontal_speed
        if self.center_x > self.player.center_x:
            self.center_x -= self.horizontal_speed
        if self.player.center_x - 10 <= self.center_x <= self.player.center_x + 10:
            self.on_search = False
            self.on_attack = True


    def hammer_player(self):
      
        self.center_y -= self.hammering_speed
        #if self.center_y < 20: # ! if == 20 it will go beyond limit 
        for wall in self.walls:
            if wall.collides_with_point((self.center_x, self.bottom)): # TODO try left and right most coord of the sprite
                #print("colliding hammer!!!!!")
                self.on_attack = False
                self.on_rise = True
                #self.center_y = 20

    def rise_up(self):
        
        
        self.center_y += self.rising_speed
        if self.center_y > self.hovering_height: # ! if == self.hovering_height it will go beyond limit
            self.on_rise = False
            self.on_search = True

    def update(self, delta_time: float = 1 / 60):
        if arcade.has_line_of_sight(self.player.position,
                                            self.position,
                                            self.walls):
            if self.on_search:
                self.move_onto_player()
        if self.on_attack:
            self.hammer_player()
        if self.on_rise:
            self.rise_up()
            
class EnemyKamikadze(Enemy):


    def __init__(self, enemy_bullet_list, player, walls):
                    
        
        super().__init__(enemy_bullet_list=enemy_bullet_list, 
                        enemy_type="kamikadze")
        
        self.x_lim = [50, 750]
        self.y_lim = [500, 550] 
        self.center_x = random.randint(self.x_lim[0], self.x_lim[1])
        self.center_y = random.randint(self.y_lim[0], self.y_lim[1]) 
        self.player = player
        self.speed = 4
        self.lives = 1
        self.position_list = None
        self.cur_position = 0
        self.barrier_list = None
        self.walls = walls
        #self.on_wait = True
        self.on_attack = False
        
        self.attack_point = None
        
    def update(self):
        #print("distance: ", arcade.get_distance(self.center_x, self.center_y,
        #                       self.player.center_x, self.player.center_y))
        
        if arcade.get_distance(self.center_x, self.center_y,
                               self.player.center_x, self.player.center_y) < 300 and \
            arcade.has_line_of_sight(self.player.position,
                                                self.position,
                                                self.walls):
            
            #self.on_wait = False
            self.on_attack = True
            self.attack_point = (self.player.center_x, self.player.center_y)
        
        if self.on_attack:
            self.rush_to_a_single_point(new_pos_x=self.attack_point[0], new_pos_y=self.attack_point[1])
            


class EnemySticker(Enemy):


    def __init__(self, enemy_bullet_list, player):
                    
        
        super().__init__(enemy_bullet_list=enemy_bullet_list, 
                        enemy_type="sticker")
        
        self.x_lim = [50, 750]
        self.y_lim = [400, 550] 
        self.center_x = random.randint(self.x_lim[0], self.x_lim[1])
        self.center_y = random.randint(self.y_lim[0], self.y_lim[1]) 
        self.player = player
        self.speed = 2
        self.lives = 3
        self.bullet = "sticker_bullet"

    def update(self):
        self.face_player()
        self.follow_sprite_on_distance()
        self.aim_and_shoot(bullet_type=self.bullet)

            
        
           
           
        
   
    
            

       
       
       
       
       
       
       
