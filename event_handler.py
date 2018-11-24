# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 15:03:01 2018

"""
import pygame as pyg
import time

class HandleEvent():
    def __init__(self):
        pass
        
    def on_input_focus(self):
        pass

    def on_input_blur(self):
        pass
    
    def on_key_down(self, event):
        if event.key == pyg.K_LEFT:
            self.xpos_change = -5    
        elif event.key == pyg.K_RIGHT:
            self.xpos_change = 5    
        elif event.key == pyg.K_DOWN:
            self. ypos_change = 5    
        elif event.key == pyg.K_UP:
            self.ypos_change = -5
        #elif pressedkeys[pyg.K_SPACE] and (cooldown == 0):
         #   for  in clip:
          #      pass
       
    def on_key_up(self, event):
        if event.key == pyg.K_LEFT or event.key == pyg.K_RIGHT:
           self.xpos_change = 0
        elif event.key == pyg.K_UP or event.key == pyg.K_DOWN:
            self.ypos_change = 0

    def text_objects(self, text, font):
        textsurface = font.render(text, True, self.black)
        return textsurface, textsurface.get_rect()

    def message_display(self, text, yloc = .45, xloc = .5):
        largetext = pyg.font.Font('freesansbold.ttf', 50)
        textsurf, textrect = self.text_objects(text, largetext)
        textrect.center = (self.width*xloc), (self.height*yloc)
        self._display_surf.blit(textsurf, textrect)
         
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
        pass
    def on_restore(self):
        pass
    def on_resize(self,event):
        pass
    def on_expose(self):
        pass

    def on_crash(self):
        self.message_display("Game Over")
        self.message_display("Press any key to try again", .65)
        pyg.display.update()
        time.sleep(1)
        while True:
            for event in pyg.event.get():
                if event.type == pyg.KEYDOWN:
                    self.xpos_change = 0
                    self.ypos_change = 0
                    self.on_execute()
                    break


    def on_exit(self):
        self._running = False

    def on_user(self,event):
        pass
    def on_event(self, event):
        # means I only ever need to use the on_event function. 
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
