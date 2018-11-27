# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 15:03:01 2018

"""
import pygame as pyg
import time
import Sprites


class HandleEvent():
    def __init__(self):
        pass

    def text_objects(self, text, font):
        textsurface = font.render(text, True, self.white)
        return textsurface, textsurface.get_rect()

    def message_display(self, text, yloc=.45, xloc=.5):
        largetext = pyg.font.Font('freesansbold.ttf', 50)
        textsurf, textrect = self.text_objects(text, largetext)
        textrect.center = (self.width * xloc), (self.height * yloc)
        self._display_surf.blit(textsurf, textrect)
        
    def on_pause(self):
        if not self.paused:
            self.paused = True
            self.message_display("GAME PAUSED", .30)
            self.message_display("Press p to unpause")
            self.message_display("Press q to quit", .65)
            pyg.display.update()
        else:
            self.paused = False

    def on_input_focus(self):
        pass

    def on_input_blur(self):
        pass
    
    def on_key_down(self, event):
        if event.key == pyg.K_LEFT:
            self.xpos_change = -5
            Sprites.player1.leftright = True
        elif event.key == pyg.K_RIGHT:
            self.xpos_change = 5   
            Sprites.player1.leftright = True
        elif event.key == pyg.K_DOWN:
            self. ypos_change = 5    
            Sprites.player1.updown = True
        elif event.key == pyg.K_UP:
            self.ypos_change = -5
            Sprites.player1.updown = True
            
        elif event.key == pyg.K_SPACE:
            reload = 0
            for bullet in Sprites.clip:
                if not bullet.alive:
                    bullet.fire(self.player_xpos, self.player_ypos)
                    reload = 5
                    break
                if reload > 0:
                    reoload -= 1
        elif event.key == pyg.K_p:
            self.on_pause()
        elif event.key == pyg.K_q:
            if self.paused:
                self.on_exit()

    def on_key_up(self, event):
        if event.key == pyg.K_LEFT or event.key == pyg.K_RIGHT:
           self.xpos_change = 0
           Sprites.player1.leftright = False
        elif event.key == pyg.K_UP or event.key == pyg.K_DOWN:
            self.ypos_change = 0
            Sprites.player1.updown = False 

    def on_mouse_focus(self):
        pass
    def on_mouse_blur(self):
        pass
    def on_mouse_move(self, event):
        pass
    def on_mouse_wheel(self, event):
        pass
    def on_lbutton_up(self, event):
        pass
    def on_lbutton_down(self, event):
        pass
    def on_rbutton_up(self, event):
        pass
    def on_rbutton_down(self, event):
        pass
    def on_mbutton_up(self, event):
        pass
    def on_mbutton_down(self, event):
        pass

    def on_minimize(self):
        self.paused = True

    def on_restore(self):
        pass

    def on_resize(self,event):
        pass
    def on_expose(self):
        pass

    def on_crash(self):
        self.lives -= 1
        if self.lives == 0:
            # play sad game over music
            self.message_display("Game Over")
            self.message_display("Press any key to try again", .65)
            pyg.display.update()
            time.sleep(1.5)
            while True:
                for event in pyg.event.get():
                    if event.type == pyg.KEYDOWN:
                        self.xpos_change = 0
                        self.ypos_change = 0
                        for aliens in Sprites.swarm:
                            aliens.alive = False
                        for bullet in Sprites.clip:
                            bullet.alive = False
                        self.on_execute()
                        break
        else:
            # bad explosion noise / Oh god no
            self.player_xpos = Sprites.BORDER
            self.player_ypos = Sprites.HEIGHT // 2
            for aliens in Sprites.swarm:
                aliens.alive = False
            self._player_hitbox = pyg.Rect(self.player_xpos, self.player_ypos,
                                           Sprites.player1.ln, Sprites.player1.ht)

    def on_exit(self):
        self._running = False

    def on_user(self,event):
        pass
    def on_event(self, event):
        # means you only ever need to use the on_event function.
        # runs all the event types as a master event
        if event.type == pyg.QUIT:
            self.on_exit()
 
        elif event.type >= pyg.USEREVENT:
            self.on_user(event)
 
        elif event.type == pyg.VIDEOEXPOSE:
            self.on_expose()
 
        elif event.type == pyg.VIDEORESIZE:
            self.on_resize(event)
 
        elif event.type == pyg.KEYUP:
            self.on_key_up(event)
                
        elif event.type == pyg.KEYDOWN:
            self.on_key_down(event)
 
        elif event.type == pyg.MOUSEMOTION:
            self.on_mouse_move(event)
 
        elif event.type == pyg.MOUSEBUTTONUP:
            if event.button == 0:
                self.on_lbutton_up(event)
            elif event.button == 1:
                self.on_mbutton_up(event)
            elif event.button == 2:
                self.on_rbutton_up(event)
 
        elif event.type == pyg.MOUSEBUTTONDOWN:
            if event.button == 0:
                self.on_lbutton_down(event)
            elif event.button == 1:
                self.on_mbutton_down(event)
            elif event.button == 2:
                self.on_rbutton_down(event)
 
        elif event.type == pyg.ACTIVEEVENT:
            if event.state == 1:
                if event.gain:
                    self.on_mouse_focus()
                else:
                    self.on_mouse_blur()
            elif event.state == 2:
                if event.gain:
                    self.on_input_focus()
                else:
                    self.on_input_blur()
            elif event.state == 4:
                if event.gain:
                    self.on_restore()
                else:
                    self.on_minimize()
 

if __name__ == "__main__" :
    event = HandleEvent()
