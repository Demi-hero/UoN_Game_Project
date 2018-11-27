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
        self.size = self.width, self.height = Sprites.WIDTH, Sprites.HEIGHT
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.xpos_change = 0
        self.ypos_change = 0
        self.move = False
        self.score = 0
        self.lives = 0
        self.paused = False

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
#        self._backgroud_image = Sprites.background.background
        self._image_surf = Sprites.player1.ship
        self.player_xpos = Sprites.BORDER
        self.player_ypos = Sprites.HEIGHT // 2
        self._player_hitbox = pyg.Rect(self.player_xpos, self.player_ypos,
                                       Sprites.player1.ln, Sprites.player1.ht)
        return True

    # what to do after this event loop
    def on_loop(self):
        # player changes
        if self.player_xpos > self.width - Sprites.player1.ln or self.player_xpos < 0:
            self.player_xpos -= (2*self.xpos_change)
        else:
            self.player_xpos += self.xpos_change
        if self.player_ypos > self.height - Sprites.player1.ht or self.player_ypos < 0:
            self.player_ypos -= (2*self.ypos_change)
        else:
            self.player_ypos += self.ypos_change
        self._player_hitbox = pyg.Rect(self.player_xpos, self.player_ypos, 
                                       Sprites.player1.ln, Sprites.player1.ht)
        
        # y-axis loop animation counter control      
        if Sprites.player1.flight_y + 1 >= 9:
            Sprites.player1.flight_y = 0
            
        # x-axis loop animation counter control      
        if Sprites.player1.flight_x + 1 >= 9:
            Sprites.player1.flight_x = 0
        
        # bullet changes
        for bullet in Sprites.clip:
            if bullet.alive and not self.paused:
                bullet.x += bullet.vx
                bullet.hitbox = pyg.Rect(bullet.x, bullet.y, bullet.ln, bullet.ht)
            if bullet.x > Sprites.WIDTH:
                bullet.alive = False
            if not bullet.alive:
                bullet.x = 0
                bullet.y = 0
                bullet.hitbox = pyg.Rect(bullet.x, bullet.y, bullet.ln, bullet.ht)

        # swarm updates
        for alien in Sprites.swarm:
            spawn_rate = 1
            if randint(1, 100) <= spawn_rate:
                alien.spawn()
            for bullet in Sprites.clip:
                if alien.hitbox.colliderect(bullet.hitbox):
                    alien.alive = False
                    bullet.alive = False
                    self.score += 50
            if alien.hitbox.colliderect(self._player_hitbox):
                self.on_crash()
            if alien.alive and not self.paused:
                alien.x += alien.vx
                alien.hitbox = pyg.Rect(alien.x, alien.y, alien.ln, alien.ht)
            if alien.x < (0 - alien.ln):
                alien.alive = False
                self.score -= 50
            if not alien.alive:
                alien.x = Sprites.WIDTH + 10
                alien.y = 0
                alien.hitbox = pyg.Rect(alien.x, alien.y, alien.ln, alien.ht)

    # what to do when images render
    def on_render(self):
        if not self.paused:
            self._display_surf.fill(self.white)
            self._display_surf.blit(Sprites.background.bg1, (Sprites.background.bg1_x, 0))
            self._display_surf.blit(Sprites.background.bg2, (Sprites.background.bg2_x, 0))
    #        self._display_surf.blit(self._backgroud_image, (0, 0))
    #        self._display_surf.blit(self._image_surf, (self.player_xpos,
    #                                                   self.player_ypos))
            
            # animate thurst on up or down
            if Sprites.player1.updown:
                self._display_surf.blit(Sprites.player1.shiptop[Sprites.player1.flight_y//3],
                                        (self.player_xpos, self.player_ypos))
                Sprites.player1.flight_y += 1
    #        else:
    #            self._display_surf.blit(self._image_surf, (self.player_xpos,
    #                                                   self.player_ypos))
            
            # animate thrust on left or right
            elif Sprites.player1.leftright:
                self._display_surf.blit(Sprites.player1.shipside[Sprites.player1.flight_x//3],
                                        (self.player_xpos, self.player_ypos))
                Sprites.player1.flight_x += 1
            else:
                self._display_surf.blit(self._image_surf, (self.player_xpos,
                                                       self.player_ypos))
                
                
            for bullet in Sprites.clip:
                if bullet.alive:
                    self._display_surf.blit(bullet.bull, (bullet.x, bullet.y))
            for alien in Sprites.swarm:
                if alien.alive:
                    self._display_surf.blit(alien.ship, (alien.x, alien.y))
            self.message_display("Score:{}".format(self.score), 0.05, 0.1)
            self.message_display("Lives: {}".format(self.lives), 0.05, .85)
            self.clock.tick(60)
            pyg.display.flip()
            
            Sprites.background.bg1_x -= 1
            Sprites.background.bg2_x -= 1

            if Sprites.background.bg1_x <= -1 * Sprites.background.bg1.get_width():
                Sprites.background.bg1_x = Sprites.background.bg2_x + Sprites.background.bg2.get_width()
            if Sprites.background.bg2_x <= -1 * Sprites.background.bg2.get_width():
                Sprites.background.bg2_x = Sprites.background.bg1_x + Sprites.background.bg1.get_width()
    # what to do when clearing images
    def on_cleanup(self):
        pyg.quit()
        quit()

    # what to do when exicuting the file.
    def on_execute(self):
        self.lives = 3
        self.score = 0
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
