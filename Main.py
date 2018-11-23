# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 13:20:18 2018

ToDo: 
    Make it stop on the edges / game over on the edge


    Make a Start screen
        Press x to play
        Credits?
        Different Music?

    Make a Game Over Screen
        Display Text to screen
        Credits?
        Music
        High Score File
"""

import pygame as pyg
import event_handler as EH
# import images
import time




class App(EH.HandleEvent):
    # initialisation
    def __init__(self, *arg, **karg):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self.size =self.width, self.height = 640, 400
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.xpos_change = 0
        self.ypos_change = 0
        self.move = False
        self.player_width = 15
        self.player_height = 12

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
        
        # loads the single image in to the image_surf variable
        self._image_surf = pyg.image.load("Single_Old_Hero.png")
        self.player_xpos = self.width * .5
        self.player_ypos = self.height * .75
        return True

    def text_objects(self, text, font):
        textsurface = font.render(text, True, self.black)
        return textsurface, textsurface.get_rect()

    def message_display(self, text, yloc = .45, xloc = .5):
        largetext = pyg.font.Font('freesansbold.ttf', 50)
        textsurf, textrect = self.text_objects(text, largetext)
        textrect.center = (self.width*xloc), (self.height*yloc)
        self._display_surf.blit(textsurf, textrect)

    def on_crash(self):
        self.message_display("Game Over")
        self.message_display("Try Again!", .65)
        pyg.display.update()
        time.sleep(2)
        self.on_execute()

    # what to do after this event loop    
    def on_loop(self):
        self.clock.tick(60)
        if self.player_xpos > self.width - self.player_width or self.player_xpos < 0:
            self.on_crash()
        if self.player_ypos > self.height - self.player_height or self.player_ypos < 0:
            self.on_crash()


    # what to do when images render
    def on_render(self):
        self.player_xpos += self.xpos_change
        self.player_ypos += self.ypos_change
        self._display_surf.fill(self.white)
        self._display_surf.blit(self._image_surf, (self.player_xpos,
                                                  self.player_ypos))
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

