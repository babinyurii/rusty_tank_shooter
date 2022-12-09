import arcade
import os

PATH_TO_SRITES = "../resources/sprites/"

def load_animation(anim_type, anim_obj):
    textures = []
    path_to_load = PATH_TO_SRITES + anim_type + "/" + anim_obj + "/"
    
    list = os.listdir(path_to_load) 
    number_of_files = len(list)
    for i in range(1, number_of_files + 1):
        texture = arcade.load_texture(path_to_load +  anim_obj + "_" + str(i) + ".png")
        textures.append(texture)
    
    
    return textures
    
    
    