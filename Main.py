# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 13:20:18 2018

ToDo: 
    Make it stop on the edges / game over on the edge
    Make a Start screen
        Press KEY to play : Can be implimented from current code
        Credits?
        Different Music?
    Make a Game Over Screen
        Display Text to screen : Done
        Credits?
        Music
        High Score File
"""

import pygame as pyg
import event_handler as EH
import Sprites
from random import randint

class App(EH.HandleEvent):
    # initialisation
    def __init__(self, *arg, **karg):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self._backgroud_image = None
        self.size =self.width, self.height = Sprites.WIDTH, Sprites.HEIGHT
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.xpos_change = 0
        self.ypos_change = 0
        self.move = False
        self.points = 0
        # self.clip = [aa, ab, ac, ad, ae]

    # do on initialisation
    def on_init(self):
        pyg.init()
        self._display_surf = pyg.display.set_mode(self.size,
                                                     pyg.HWSURFACE)
        # sets the window name
        self._running = True
        pyg.display.set_caption('A Try Force Production')
        
        # this is how I manage the frames per second
        self.clock = pyg.time.Clock()

        # loads the images in to the related image_surf variable
        self._backgroud_image = Sprites.background.background
        self._image_surf = Sprites.player1.ship
        self.player_xpos = Sprites.BORDER
        self.player_ypos = Sprites.HEIGHT//2
        return True


    # what to do after this event loop    
    def on_loop(self):
        pass



    # what to do when images render
    def on_render(self):

        if self.player_xpos > self.width - Sprites.player1.ln or self.player_xpos < 0:
            self.player_xpos -= (2*self.xpos_change)
        else:
            self.player_xpos += self.xpos_change
        if self.player_ypos > self.height - Sprites.player1.ht or self.player_ypos < 0:
            self.player_ypos -= (2*self.ypos_change)
        else:
            self.player_ypos += self.ypos_change
        self._display_surf.fill(self.white)
        self._display_surf.blit(self._backgroud_image, (0, 0))
        self._display_surf.blit(self._image_surf, (self.player_xpos,
                                                  self.player_ypos))
        # make this neater ? Is how we handle bullet progresion
        for bullet in Sprites.clip:
            if bullet.alive:
                bullet.x += bullet.vx
                bullet.hitbox = pyg.Rect(bullet.x, bullet.y, bullet.ln, bullet.ht)
                self._display_surf.blit(bullet.bull, (bullet.x, bullet.y))
            if bullet.x > Sprites.WIDTH:
                bullet.alive = False
            if not bullet.alive:
                bullet.x = 0
                bullet.y = 0


        for alien in Sprites.swarm:
            spawn_rate = 1
            if randint(1,75) <= spawn_rate:
                alien.spawn()
            if alien.alive:
                alien.x += alien.vx
                alien.hitbox = pyg.Rect(alien.x, alien.y, alien.ln, alien.ht)
                self._display_surf.blit(alien.ship, (alien.x, alien.y))
            if alien.x < (0-alien.ln):
                alien.alive == False
            if not alien.alive:
                alien.x = Sprites.WIDTH + 10
                alien.y = 0
                alien.hitbox = pyg.Rect(alien.x, alien.y, alien.ln, alien.ht)
        self.clock.tick(60)
        pyg.display.flip()

    # what to do when clearing images
    def on_cleanup(self):
        pyg.quit()

    # what to do when exicuting the file.
    def on_execute(self):
        if not self.on_init():
            self._running = False

        while self._running:
            for event in pyg.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()


if __name__ == '__main__':
    theApp = App()
    theApp.on_execute()
