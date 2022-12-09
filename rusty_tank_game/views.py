# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 18:37:13 2022

@author: yuriy
"""
import arcade
from constants import *
            
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



