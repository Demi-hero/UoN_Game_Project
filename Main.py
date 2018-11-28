import pygame as pyg
import os
from gamedata import *
from eventhandler import *

class Main(HandleEvent):

    def __init__(self):
        self.startup = True
        self.running = True
        self.paused = False
        self.lives = 3
        self.score = 0
        self.clock = pyg.time.Clock()
        self.framerate = 100
        # objects created inside the class. Not sure if this is a good thing or not?
        self.Files = FileStore()
        self.Board = Background()
        self.Player1 = Player()
        self.Bullet1 = Bullet()
        self.Alien1 = Alien()

    # will need refactoring to match rest of code style is how the code handles start up
    def on_startup(self):
        self.Board.update()
        # self.message_display("Highscores :",xloc=.35)
        # self.message_display(" Lore :", xloc=.65)
        self.message_display("Movement", yloc=.57, xloc=.26)
        self.message_display("Shoot", yloc=.65, xloc=.7)
        self.Board.screen.blit(self.Files.title, (221, 0))
        self.Board.screen.blit(self.Files.arrows, (160, 320))
        # gamedata.background.screen.blit(Game_Data.startup.h, (425, 228))
        # gamedata.background.screen.blit(Game_Data.startup.l, (675, 228))
        self.Board.screen.blit(self.Files.space, (591, 375))
        self.message_display("Press Shoot to Start", .9, font_size=35)
        pyg.display.flip()
        while self.startup:
            for event in pyg.event.get():
                self.on_event(event)
            pyg.display.flip()

    def execute(self):
        pyg.init()
        # creating the screen and game objects

        while self.startup:
            self.on_startup()

        # main game loop
        while self.running:
            # taking the player input, passing to event handler
            for event in pyg.event.get():
                self.on_event(event, self.Player1, self.Bullet1)
            self.player_movement(self.Player1)

            # updating the object states, and drawing to screen (see gamedata)
            if not self.paused:
                self.Board.update()
                self.Player1.update()
                self.Bullet1.update()
                # passes main (self) to alien update and detect_collision to update score and lives
                self.Alien1.update(self)
                # detecting collisions between aliens and bullets, and aliens and player
                self.Alien1.detect_collisions(self.Player1, self.Bullet1, self)

                # display lives and score at top of screen
                self.message_display("Score:{}".format(self.score), 0.03, 0.1, 20)
                self.message_display("Lives: {}".format(self.lives), 0.03, .85, 20)

                # if out of lives - game over (see eventhandler)
                if self.lives < 1:
                    self.gameover(self.Player1, self.Bullet1, self.Alien1)

                # update the display
                pyg.display.flip()
                self.clock.tick(self.framerate)

App = Main()
App.execute()
pyg.quit()
os._exit(0)
