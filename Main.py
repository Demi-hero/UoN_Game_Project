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
        self.player_width = Sprites.player1.ln
        self.player_height = Sprites.player1.ht
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
        self.player_xpos = self.width * .5
        self.player_ypos = self.height * .75
        return True


    # what to do after this event loop    
    def on_loop(self):
        pass



    # what to do when images render
    def on_render(self):

        if self.player_xpos > self.width - self.player_width or self.player_xpos < 0:
            self.player_xpos -= (2*self.xpos_change)
        else:
            self.player_xpos += self.xpos_change
        if self.player_ypos > self.height - self.player_height or self.player_ypos < 0:
            self.player_ypos -= (2*self.ypos_change)
        else:
            self.player_ypos += self.ypos_change
        self._display_surf.fill(self.white)
        self._display_surf.blit(self._backgroud_image, (0, 0))
        self._display_surf.blit(self._image_surf, (self.player_xpos,
                                                  self.player_ypos))
        for bullet in Sprites.clip:
            if bullet.alive:
                bullet.x += bullet.vx
                self._display_surf.blit(bullet.bull, (bullet.x, bullet.y))
            if bullet.x > Sprites.WIDTH:
                bullet.alive = False
            if not bullet.alive:
                bullet.x = 0
                bullet.y = 0
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
