import arcade
import random
import math

# --- Explosion Particles Related
# How fast the particle will accelerate down. Make 0 if not desired
#PARTICLE_GRAVITY = 0.05
# How fast to fade the particle
#PARTICLE_FADE_RATE = 10
# How fast the particle moves. Range is from 2.5 <--> 5 with 2.5 and 2.5 set.
#PARTICLE_MIN_SPEED = 2.5
#PARTICLE_SPEED_RANGE = 2.5
# How many particles per explosion
#PARTICLE_COUNT = 20
# How big the particle
#PARTICLE_RADIUS = 5
# Possible particle colors

# Chance we'll flip the texture to white and make it 'sparkle'
PARTICLE_SPARKLE_CHANCE = 0.2



            

class Particle(arcade.SpriteCircle):
    """ Explosion particle """
    def __init__(self, radius, color, direction):
        super().__init__(radius=radius, color=color)
        
        self.fade_rate = 10
        self.speed_range = 2.5
        self.min_speed = 2.5
        self.gravity = 0.05

        # Track normal particle texture, so we can 'flip' when we sparkle.
        self.normal_texture = self.texture
        # Keep track of the list we are in, so we can add a smoke trail
        #self.my_list = my_list
        # Set direction/speed
        speed = random.random() * self.speed_range + self.min_speed
        self.direction = random.randrange(direction)
        self.change_x = (math.sin(math.radians(self.direction)) * speed)
        self.change_y = (math.cos(math.radians(self.direction)) * speed)
        # Track original alpha. Used as part of 'sparkle' where we temp set the
        # alpha back to 255
        self.my_alpha = 255
        # What list do we add smoke particles to?
        #self.my_list = my_list

    def update(self):
        """ Update the particle """
        if self.my_alpha <= self.fade_rate:
            # Faded out, remove
            self.remove_from_sprite_lists()
        else:
            # Update
            self.my_alpha -= self.fade_rate
            self.alpha = self.my_alpha
            self.center_x += self.change_x
            self.center_y += self.change_y
            self.change_y -= self.gravity

            #Should we sparkle this?
            if random.random() <= PARTICLE_SPARKLE_CHANCE:
                self.alpha = 255
                self.texture = arcade.make_circle_texture(int(self.width),
                                                          arcade.color.ORANGE)
            else:
                self.texture = self.normal_texture

            # Leave a smoke particle?
            #if random.random() <= SMOKE_CHANCE:
            #    smoke = Smoke(5)
            #    smoke.position = self.position
            #    self.my_list.append(smoke)




class RectangularParticle(arcade.SpriteSolidColor):
    """ Explosion particle """

    

    def __init__(self, width, height, color, direction, angle_rotation_speed):
        
       

        super().__init__(width=width, height=height, color=color)
        
        self.fade_rate = 10
        self.speed_range = 2.5
        self.min_speed = 2.5
        self.gravity = 0.05
        #self.angle_rotation_speed = random.randint(0, 25)
        self.angle_rotation_speed = angle_rotation_speed
        rotation_direction = random.choice(["clock_wise", "counter_clock_wise"])
        self.angle_rotation_direction = rotation_direction

        # Track normal particle texture, so we can 'flip' when we sparkle.
        #self.normal_texture = self.texture
        # Keep track of the list we are in, so we can add a smoke trail
        #self.my_list = my_list
        # Set direction/speed
        speed = random.random() * self.speed_range + self.min_speed
        self.direction = random.randrange(direction)
        self.change_x = (math.sin(math.radians(self.direction)) * speed)
        self.change_y = (math.cos(math.radians(self.direction)) * speed)
        # Track original alpha. Used as part of 'sparkle' where we temp set the
        # alpha back to 255
        self.my_alpha = 255
        # What list do we add smoke particles to?
        #self.my_list = my_list

    def update(self):
        """ Update the particle """
        if self.my_alpha <= self.fade_rate:
            # Faded out, remove
            self.remove_from_sprite_lists()
        else:
            # Update
            self.my_alpha -= self.fade_rate
            self.alpha = self.my_alpha
            self.center_x += self.change_x
            self.center_y += self.change_y
            self.change_y -= self.gravity
            # good parameter to make it look nice: rotating sprtie
            if self.angle_rotation_direction == "clock_wise":
                self.angle += self.angle_rotation_speed
            elif self.angle_rotation_direction == "counter_clock_wise":
                self.angle -= self.angle_rotation_speed
                
                

class RectangularParticleDisappearOnSize(arcade.SpriteSolidColor):
    """ Explosion particle """

    

    def __init__(self, width, height, color, direction, angle_rotation_speed):
        
       

        super().__init__(width=width, height=height, color=color)
        
        self.fade_rate = 10
        self.speed_range = 2.5
        self.min_speed = 2.5
        self.gravity = 0.05
        #self.angle_rotation_speed = random.randint(0, 25)
        self.angle_rotation_speed = angle_rotation_speed
        rotation_direction = random.choice(["clock_wise", "counter_clock_wise"])
        self.angle_rotation_direction = rotation_direction

        # Track normal particle texture, so we can 'flip' when we sparkle.
        #self.normal_texture = self.texture
        # Keep track of the list we are in, so we can add a smoke trail
        #self.my_list = my_list
        # Set direction/speed
        speed = random.random() * self.speed_range + self.min_speed
        self.direction = random.randrange(direction)
        self.change_x = (math.sin(math.radians(self.direction)) * speed)
        self.change_y = (math.cos(math.radians(self.direction)) * speed)
        # Track original alpha. Used as part of 'sparkle' where we temp set the
        # alpha back to 255
        self.my_alpha = 255
        # What list do we add smoke particles to?
        #self.my_list = my_list

    def update(self):
        """ Update the particle """
        #if self.my_alpha <= self.fade_rate:
            # Faded out, remove
        #if self.width or self.height <= 1: # TODO ??? if here's or, they just disappear after their appearance, in a point
        #    self.remove_from_sprite_lists()
        if self.width <= 2:
            self.remove_from_sprite_lists()
        elif self.height <=2:
            self.remove_from_sprite_lists()
        else:
            # Update
            #self.my_alpha -= self.fade_rate
            #self.alpha = self.my_alpha
            self.width -= 1
            self.height -= 1
            self.center_x += self.change_x
            self.center_y += self.change_y
            self.change_y -= self.gravity
            # good parameter to make it look nice: rotating sprtie
            if self.angle_rotation_direction == "clock_wise":
                self.angle += self.angle_rotation_speed
            elif self.angle_rotation_direction == "counter_clock_wise":
                self.angle -= self.angle_rotation_speed