from particle_types import ParticleCircleStillAlpha, ParticleRectStillAlpha, ParticleRectMoveSize, ParticleRectMoveAlphaIncrease, \
    EnemyExplosionOnSize, GroundHitByEnemyBullet, PlayerShotParticle, \
    ParticleStill, RectangularParticle
import random
import arcade


def add_hover_trace_to_player_bullet(bullet_center_x, bullet_bottom_y, explosion_layer):
    for i in range(1):
        particle = ParticleCircleStillAlpha(radius=2, 
                                            color=arcade.color.WHITE_SMOKE,
                                            fade_rate=(random.randint(1,255)),
                                            gravity=0.5)
        
        bullet_center_x += random.randint(-5, 5)
        particle.position = bullet_center_x, bullet_bottom_y
        explosion_layer.append(particle)
        
def add_hover_rect_trace_to_player_bullet(bullet_center_x, bullet_bottom_y, explosion_layer):
    for i in range(1):
        particle = ParticleRectStillAlpha(width=random.randint(1,10),
                                                 height=random.randint(1,10), 
                                            color=arcade.color.GRAY,
                                            fade_rate=(random.randint(1,255)),
                                            gravity=0.5)
        
        bullet_center_x += random.randint(-5, 5)
        particle.position = bullet_center_x, bullet_bottom_y
        explosion_layer.append(particle)

        
def add_trace_to_player_bullet(bullet_center_x, bullet_bottom_y, explosion_layer):
    for i in range(1):
        particle = ParticleStill()
        particle.position = bullet_center_x, bullet_bottom_y
        explosion_layer.append(particle)
        

    

def explode_enemy(explosion_list, explosion_layer):
    
    for obj in explosion_list:
        for particle_num in range(10):
            particle = ParticleRectMoveSize(width=random.randint(10, 15),
                                                          height=random.randint(10,15),
                                                          color=arcade.color.RED,
                                                          direction=random.randint(1,360),
                                                          speed=random.randint(1,10),
                                                          rotation_speed=random.randint(1,10),
                                                          gravity=0.0,
                                                          size_change=1)
            particle.position = obj.position
            explosion_layer.append(particle)



def reverse_explode(obj_center_x, obj_center_y, explosion_layer):
    """function for enemy appearance"""
    
    particle_positions = [[obj_center_x + 150, obj_center_y],
                           [obj_center_x - 150, obj_center_y],
                           [obj_center_x, obj_center_y + 150],
                           [obj_center_x, obj_center_y - 150],
                           [obj_center_x + 80, obj_center_y + 80],
                           [obj_center_x + 80, obj_center_y - 80],
                           [obj_center_x - 80, obj_center_y - 80],
                           [obj_center_x - 80, obj_center_y + 80]]   
    
    for i in particle_positions:
        particle = ParticleRectMoveAlphaIncrease(width=20, height=20, color=arcade.color.YELLOW,
                                                 speed=8, rotation_speed=20, gravity=0.0,
                                                 destination_x=obj_center_x, 
                                                 destination_y=obj_center_y,
                                                 color_saturation_rate=10)
        particle.center_x = i[0]
        particle.center_y = i[1]
        explosion_layer.append(particle)
    
    

###############################################3
########################################################
# old variants
#########################################################3
########################################################

  

def explode_particles_in_circle_out(explosion_list, explosion_layer):
    
    for obj in explosion_list:
        print("obj position: ", obj.position)
        for i in range(1, 360, 20):
            width = random.randint(2, 20)
            height = random.randint(2, 20)
            color = random.choice([arcade.color.WHITE_SMOKE, arcade.color.GRAY]) 
            direction = i
            angle_rotation_speed = random.randint(1, 10)
            # !!! give the position in init of the particle, otherwise it goes somehow to the 0,0 coords
            particle = RectangularParticle(width=width, height=height, color=color,
                                           direction=direction, 
                                           angle_rotation_speed=angle_rotation_speed,
                                           center_x=obj.center_x,
                                           center_y=obj.center_y)
            #particle.positon = obj.position
            explosion_layer.append(particle)
        


###################################################
###################################################
###################################################
###################################################
# old variants


def explode_enemy_1(explosion_list, explosion_layer):
    
    for obj in explosion_list:
        for particle_num in range(10):
            particle = EnemyExplosionOnSize()
            particle.position = obj.position
            explosion_layer.append(particle)
            

def player_shot_burst(player_center_x, player_top_y, explosion_layer):
    
    for i in range(5):
        particle = PlayerShotParticle()
        particle.position = player_center_x, player_top_y
        explosion_layer.append(particle)


       
            
            
    
        
