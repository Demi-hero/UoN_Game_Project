# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 15:03:01 2018

"""
import pygame as pyg
import time
import Game_Data
from os import path
import csv


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
    def create_false_hs(self):
        with open("highscore.csv", "w", newline='') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=",")
            filewriter.writerow(["Jes", "3200"])
            filewriter.writerow(["Peter", "2200"])
            filewriter.writerow(["Nate", "1200"])
            self.scores = [["Jes", "3200"], ["Peter", "2200"], ["Nate", "1200"], ["backstop","0"]]
            self.high_score = int(self.scores[0][1])

    def load_data(self):
        self.scores = []
        try:
            # have used with to double make sure I closed the file
            with open("highScore.csv", "r", newline='') as f:
                reader = csv.reader(f, delimiter=',')
                for row in reader:
                    self.scores.append(row)
                print(self.scores)
                self.high_score = int(self.scores[0][1])
        except FileNotFoundError:
            self.create_false_hs()
            print("FnF error")
        except ValueError:
            print("Value Error")
            self.create_false_hs()
        except IndexError:
            print("I am confused")
            self.create_false_hs()

    def game_over_display(self):
        self._display_surf.blit(Game_Data.background.bg1, (Game_Data.background.bg1_x, 0))
        self._display_surf.blit(Game_Data.background.bg2, (Game_Data.background.bg2_x, 0))
        self.message_display("Game Over", 0.35)
        self.message_display("Player Name: {}".format(Game_Data.player1.player_name), .5, .5)
        pyg.display.flip()

    def scorboard_check(self):
        for lists in self.scores:
            if self.score > int(lists[1]):
                return True
        return False

    def on_new_highscore(self):
        self.altering_name = True
        self.high_score = self.score
        self.message_display("NEW HIGH SCORE: {}!".format(self.score), .55)
        while self.altering_name:
            for event in pyg.event.get():
                if event.type == pyg.KEYDOWN:
                    if event.unicode.isalpha():
                        Game_Data.player1.update_name(event.unicode)
                    elif event.key == pyg.K_BACKSPACE:
                        Game_Data.player1.update_name("", 1)
                    elif event.key == pyg.K_RETURN:
                        if len(Game_Data.player1.player_name) < 3:
                            Game_Data.player1.update_name()
                        else:
                            self.scoreboard = [Game_Data.player1.player_name, self.score]
                            self.altering_name = False
                elif event.type == pyg.QUIT:
                    pyg.quit()
                    quit()
                self.game_over_display()
        with open("highscore.csv", "w", newline='') as f:
            scorewriter = csv.writer(f, delimiter=',')
            for value, lists in enumerate(self.scores):
                if self.scoreboard[1] > int(lists[1]):
                    self.scores.insert(value, self.scoreboard)
                    break
            if len(self.scores) > 10:
                self.scores[:] = self.scores[:-1]
            for lists in self.scores:
                print(lists)
                scorewriter.writerow((lists[0], lists[1]))

    def on_pause(self, minimised=0):
        if not self.paused:
            self.paused = True
            self.message_display("GAME PAUSED", .30)
            self.message_display("Press p to unpause")
            self.message_display("Press q to quit", .65)
            pyg.display.update()
        elif not minimised:
            self.paused = False

    def on_input_focus(self):
        pass

    def on_input_blur(self):
        pass
    
    def on_key_down(self, event):
        if event.key == pyg.K_LEFT:
            self.xpos_change = -5
            Game_Data.player1.leftright = True
        elif event.key == pyg.K_RIGHT:
            self.xpos_change = 5   
            Game_Data.player1.leftright = True
        elif event.key == pyg.K_DOWN:
            self. ypos_change = 5    
            Game_Data.player1.updown = True
        elif event.key == pyg.K_UP:
            self.ypos_change = -5
            Game_Data.player1.updown = True
            
        elif event.key == pyg.K_SPACE:
            reload = 0
            for bullet in Game_Data.clip:
                if not bullet.alive:
                    bullet.fire(self.player_xpos, self.player_ypos)
                    reload = 5
                    break
                if reload > 0:
                    reload -= 1
        elif event.key == pyg.K_p:
            self.on_pause()
        elif event.key == pyg.K_q:
            if self.paused:
                self.on_exit()

    def on_key_up(self, event):
        if event.key == pyg.K_LEFT or event.key == pyg.K_RIGHT:
           self.xpos_change = 0
           Game_Data.player1.leftright = False
        elif event.key == pyg.K_UP or event.key == pyg.K_DOWN:
            self.ypos_change = 0
            Game_Data.player1.updown = False

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
        self.on_pause(1)

    def on_restore(self):
        print("I was run")

    def on_resize(self,event):
        pass

    def on_expose(self):
        pass

    def on_crash(self):
        self.lives -= 1
        if self.lives == 0:
            # play sad game over music
            if self.scorboard_check():
                self.on_new_highscore()
            else:
                self.message_display("Highscore: {}".format(self.high_score))
                self.message_display("Your Score: {}".format(self.score), .55)

            self.message_display("Press any key to try again", .65)
            pyg.display.update()
            time.sleep(1.5)
            while True:
                for event in pyg.event.get():
                    if event.type == pyg.QUIT:
                        self.on_execute()
                    elif event.type == pyg.KEYDOWN:
                        self.xpos_change = 0
                        self.ypos_change = 0
                        for aliens in Game_Data.swarm:
                            aliens.alive = False
                        for bullet in Game_Data.clip:
                            bullet.alive = False
                        self.on_execute()
                        break
        else:
            # bad explosion noise / Oh god no
            self.player_xpos = Game_Data.BORDER
            self.player_ypos = Game_Data.HEIGHT // 2
            for aliens in Game_Data.swarm:
                aliens.alive = False
            self._player_hitbox = pyg.Rect(self.player_xpos, self.player_ypos,
                                           Game_Data.player1.ln, Game_Data.player1.ht)

    def on_exit(self):
        self._running = False

    def on_user(self, event):
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
            elif event.state == 6:
                if not event.gain:
                    self.on_minimize()
            elif event.state == 4:
                if event.gain:
                    self.on_restore()
 

if __name__ == "__main__" :
    event = HandleEvent()
