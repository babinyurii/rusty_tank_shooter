from particle import Particle, RectangularParticleDisappearOnSize
import random
import arcade
import math




class ParticleCircleStillAlpha(arcade.SpriteCircle):
    """ Explosion particle """
    def __init__(self, radius, color, fade_rate, gravity):
        
        super().__init__(radius=radius, color=color)
        self.my_alpha = 255
        self.fade_rate = fade_rate
        self.gravity = gravity
        
    def update(self):
        """ Update the particle """
        if self.my_alpha <= self.fade_rate:
            self.remove_from_sprite_lists()
        else:
            #update
            self.my_alpha -= self.fade_rate
            self.alpha = self.my_alpha
            self.center_y -= self.gravity
            
            
class ParticleCircleStillSizeShrink(arcade.SpriteCircle):
    """ Explosion particle """
    def __init__(self, radius, color, radius_change, radius_limit, gravity):
        
        super().__init__(radius=radius, color=color)
        self.radius_change = radius_change
        self.radius_limit = radius_limit
        self.gravity = gravity
        
    def update(self):
        """ Update the particle """
        if self.radius <= self.radius_limit:
            self.remove_from_sprite_lists()
        else:
            #update
            self.radius -= self.radius_change
            self.center_y -= self.gravity
            
            

class ParticleRectStillAlpha(arcade.SpriteSolidColor):
    """ Explosion particle """
    def __init__(self, width, height, color, fade_rate, gravity):
        
        super().__init__(width=width, height=height, color=color)
        self.my_alpha = 255
        self.fade_rate = fade_rate
        self.gravity = gravity
        
    def update(self):
        """ Update the particle """
        if self.my_alpha <= self.fade_rate:
            self.remove_from_sprite_lists()
        else:
            #update
            self.my_alpha -= self.fade_rate
            self.alpha = self.my_alpha
            self.center_y -= self.gravity


class ParticleRectMoveSize(arcade.SpriteSolidColor):
    """ Explosion particle """

    def __init__(self, width, height, color, direction, speed, rotation_speed, gravity, size_change):

        super().__init__(width=width, height=height, color=color)
        
        self.direction = direction
        self.speed = speed
        self.rotation_speed = rotation_speed
        self.gravity = gravity
        self.size_change = size_change
        
        rotation_direction = random.choice(["clock_wise", "counter_clock_wise"])
        self.angle_rotation_direction = rotation_direction

        self.change_x = (math.sin(math.radians(self.direction)) * speed)
        self.change_y = (math.cos(math.radians(self.direction)) * speed)


    def update(self):
        """ Update the particle """
       
        if self.width <= 2:
            self.remove_from_sprite_lists()
        elif self.height <=2:
            self.remove_from_sprite_lists()
        else:
            # Update
            self.width -= self.size_change
            self.height -= self.size_change
            self.center_x += self.change_x
            self.center_y += self.change_y
            self.change_y -= self.gravity
            # good parameter to make it look nice: rotating 
            if self.angle_rotation_direction == "clock_wise":
                self.angle += self.rotation_speed
            elif self.angle_rotation_direction == "counter_clock_wise":
                self.angle -= self.rotation_speed           


# particle primary for enemy appearance. reverse explosion
class ParticleRectMoveAlphaIncrease(arcade.SpriteSolidColor):
    """ Explosion particle """

    def __init__(self, width, height, color, speed, rotation_speed, gravity, 
                 destination_x,
                 destination_y,
                 color_saturation_rate):

        super().__init__(width=width, height=height, color=color)
        
        #self.direction = direction
        self.speed = speed
        self.rotation_speed = rotation_speed
        self.gravity = gravity
        #self.size_change = size_change
        
        rotation_direction = random.choice(["clock_wise", "counter_clock_wise"])
        self.angle_rotation_direction = rotation_direction

        #self.change_x = (math.sin(math.radians(self.direction)) * speed)
        #self.change_y = (math.cos(math.radians(self.direction)) * speed)
        self.destination_x = destination_x
        self.destination_y = destination_y
        self.color_saturation_rate = color_saturation_rate
        self.my_alpha = 0

    
    def update(self, delta_time: float = 1 / 60):    
        
        # Where are we
        start_x = self.center_x
        start_y = self.center_y

        # Where are we going
        dest_x = self.destination_x
        dest_y = self.destination_y

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
        
        self.my_alpha += self.color_saturation_rate
        if self.my_alpha > 255:
            self.my_alpha = 255
        self.alpha = self.my_alpha

        # How far are we?
        distance = math.sqrt((self.center_x - dest_x) ** 2 + (self.center_y - dest_y) ** 2)
        self.change_y -= self.gravity
        if self.angle_rotation_direction == "clock_wise":
            self.angle += self.rotation_speed
        elif self.angle_rotation_direction == "counter_clock_wise":
            self.angle -= self.rotation_speed  
                
        # If we are there, head to the next point.
        if distance <= self.speed:
            #self.on_attack = False
            #self.on_wait = True
            self.remove_from_sprite_lists()
        
        
   



#===============================================
# other obj variants, may be usefule
class ParticleRectMovingSize(arcade.SpriteSolidColor):
    """ Explosion particle """
    def __init__(self, width, height, color, fade_rate, gravity):
        
        super().__init__(width=width, height=height, color=color)
        self.my_alpha = 255
        self.fade_rate = fade_rate
        self.gravity = gravity
        
    def update(self):
        """ Update the particle """
        if self.my_alpha <= self.fade_rate:
            self.remove_from_sprite_lists()
        else:
            #update
            self.my_alpha -= self.fade_rate
            self.alpha = self.my_alpha
            self.center_y -= self.gravity
            
  
class EnemyExplosionOnSize(RectangularParticleDisappearOnSize):
    
    
      def __init__(self, direction=360):
          colors = [arcade.color.LAVA, arcade.color.RED, arcade.color.ORANGE]
          
          color = random.choice(colors)
          angle_rotation_speed = random.randint(0, 10)
          particle_width = random.randint(10, 20)
          particle_height = random.randint(10, 20)
          #particle_width = 30
          #particle_height = 30

          super().__init__(width=particle_width, height=particle_height, color=color, direction=direction,
                              angle_rotation_speed=angle_rotation_speed)

          #self.fade_rate = 15
          self.speed_range = 5
          self.min_speed = 1
          self.gravity = 0.1    
  
    
  
            
##############################################
##########################################
##########################################3
# old variants


class ParticleStill(arcade.SpriteCircle):
    """ Explosion particle """
    def __init__(self):
        
        colors = [ arcade.color.WHITE_SMOKE]
        color = random.choice(colors)
        radius = random.randint(1, 3)
        
        super().__init__(radius=radius, color=color)

        self.my_alpha = 255
        
        self.fade_rate = 25
        self.speed_range = 0
        self.min_speed = 0
        self.gravity = 0.0
        
    def update(self):
        """ Update the particle """
        if self.my_alpha <= self.fade_rate:
            # Faded out, remove
            self.remove_from_sprite_lists()
        else:
            # Update
            self.my_alpha -= self.fade_rate
            self.alpha = self.my_alpha
            
            

class RectangularParticle(arcade.SpriteSolidColor):
    """ Explosion particle """

    

    def __init__(self, width, height, color, direction, angle_rotation_speed,
                 center_x, center_y):
        

        super().__init__(width=width, height=height, color=color)
        
        self.fade_rate = 10
        #self.speed_range = 2.5
        #self.min_speed = 2.5
       
        self.center_x = center_x
        self.center_y = center_y
        self.angle_rotation_speed = angle_rotation_speed
        rotation_direction = random.choice(["clock_wise", "counter_clock_wise"])
        self.angle_rotation_direction = rotation_direction

        #speed = random.random() * self.speed_range + self.min_speed
        speed = 5
        self.direction = direction
        self.change_x = (math.sin(math.radians(self.direction)) * speed)
        self.change_y = (math.cos(math.radians(self.direction)) * speed)
        
        
        
        self.my_alpha = 255
   

    def update(self):
        """ Update the particle """
        if self.my_alpha <= self.fade_rate:
            self.remove_from_sprite_lists()
        else:
            # Update
            self.my_alpha -= self.fade_rate
            self.alpha = self.my_alpha
            self.center_x += self.change_x
            self.center_y += self.change_y
            #self.change_y -= self.gravity
            # good parameter to make it look nice: rotating sprtie
            if self.angle_rotation_direction == "clock_wise":
                self.angle += self.angle_rotation_speed
            elif self.angle_rotation_direction == "counter_clock_wise":
                self.angle -= self.angle_rotation_speed
            
            


###################################################
###################################################
###################################################
###################################################
# old variants

class EnemyHitByPlayer(Particle):
    """ Explosion particle """
    def __init__(self, radius=2, color=arcade.color.RED, direction=360):
        super().__init__(radius=radius, color=color, direction=direction)

        self.fade_rate = 50
        self.speed_range = 2.5
        self.min_speed = 2.5
        self.gravity = 0
        

class PlayerHitByEnemy(Particle):
    """ Explosion particle """
    def __init__(self, radius=5, color=arcade.color.RED, direction=360):
        super().__init__(radius=radius, color=color, direction=direction)

        self.fade_rate = 25
        self.speed_range = 2.5
        self.min_speed = 2.5
        self.gravity = 0


class GroundHitByEnemyBullet(Particle):
    """ Explosion particle """
   
    def __init__(self, direction=360):
        colors = [arcade.color.RED, arcade.color.BLACK]
        color = random.choice(colors)
        radius = random.randint(1,3)
        super().__init__(radius=radius, color=color, direction=direction)

        self.fade_rate = 25
        self.speed_range = 30
        self.min_speed = 20
        self.gravity = 0.0
        # make particle fly upwards, at it imitates explosion on the ground
        if self.change_y < 0:
            self.change_y = self.change_y * -1

class EnemyExplosion(RectangularParticle):
    """ Explosion particle """
    
    def __init__(self, direction=360):
        colors = [arcade.color.WHITE, arcade.color.RED]
        color = random.choice(colors)
        angle_rotation_speed = random.randint(0, 10)
        particle_width = random.randint(1, 15)
        particle_height = random.randint(1, 15)

        super().__init__(width=particle_width, height=particle_height, color=color, direction=direction,
                            angle_rotation_speed=angle_rotation_speed)

        self.fade_rate = 15
        self.speed_range = 2.5
        self.min_speed = 1
        self.gravity = 0.1
        
class EnemyExplosionOnSize(RectangularParticleDisappearOnSize):
    
    
      def __init__(self, direction=360):
          colors = [arcade.color.LAVA, arcade.color.RED, arcade.color.ORANGE]
          
          color = random.choice(colors)
          angle_rotation_speed = random.randint(0, 10)
          particle_width = random.randint(10, 20)
          particle_height = random.randint(10, 20)
          #particle_width = 30
          #particle_height = 30

          super().__init__(width=particle_width, height=particle_height, color=color, direction=direction,
                              angle_rotation_speed=angle_rotation_speed)

          #self.fade_rate = 15
          self.speed_range = 5
          self.min_speed = 1
          self.gravity = 0.1
          
class PlayerShotParticle(Particle):
    """ Explosion particle """
   
    def __init__(self, direction=250):
        colors = [arcade.color.RED, arcade.color.ORANGE, arcade.color.GRAY, arcade.color.WHITE_SMOKE]
        color = random.choice(colors)
        radius = random.randint(1, 3)
        super().__init__(radius=radius, color=color, direction=direction)

        self.fade_rate = 25
        self.speed_range = 2
        self.min_speed = 1
        self.gravity = 0.0
        # make particle fly upwards, at it imitates explosion on the ground
        if self.change_y < 0:
            self.change_y = self.change_y * -1



   
   

