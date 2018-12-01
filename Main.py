import pygame as pyg
import os
# change these imports to not import *
from gamedata import *
from eventhandler import *
import time


class Main(HandleEvent):

    def __init__(self):
        self.startup = True
        self.running = True
        self.paused = False
        self.lives = 3
        self.bombs = 1
        self.score = 0
        self.clock = pyg.time.Clock()
        self.framerate = 100
        self.starttime = time.time()
        self.white = (255, 255, 255)
        # objects created inside the class. Not sure if this is a good thing or not?

    # will need refactoring to match rest of code style is how the code handles start up
    def on_startup(self, background, files):
        background.update()
        # self.message_display("Highscores :",xloc=.35)
        # self.message_display(" Lore :", xloc=.65)
        self.message_display("Movement", yloc=.57, xloc=.26)
        self.message_display("Shoot", yloc=.65, xloc=.7)
        background.screen.blit(files.title, (221, 0))
        background.screen.blit(files.arrows, (160, 320))
        # gamedata.background.screen.blit(Game_Data.startup.h, (425, 228))
        # gamedata.background.screen.blit(Game_Data.startup.l, (675, 228))
        background.screen.blit(files.space, (591, 375))
        self.message_display("Press Shoot to Start", .9, font_size=35)
        pyg.display.flip()
        while self.startup:
            for event in pyg.event.get():
                self.on_event(event, files=files)
            pyg.display.flip()

    def execute(self):
        pyg.init()
        Files = FileStore()
        Board = Background()
        Player1 = Player()
        Bullet1 = Bullet()
        Alien1 = Alien()
        power_up = PowerUp(self)

        # creating the screen and game objects

        while self.startup:
            self.on_startup(Board, Files)

        # main game loop
        while self.running:
            # taking the player input, passing to event handler
            for event in pyg.event.get():
                self.on_event(event, Board, Player1, Alien1, Bullet1, Files)
            self.player_movement(Player1)

            # updating the object states, and drawing to screen (see gamedata)
            if not self.paused:
                Board.update()
                Player1.update()
                Bullet1.update()
                power_up.spawn(Player1)
                # passes main (self) to alien update and detect_collision to update score and lives
                Alien1.update(self)
                # detecting collisions between aliens and bullets, and aliens and player
                Alien1.detect_collisions(Player1, Bullet1, self)
                # if enough time has passed and no power ups spawn a power up
                    # powerups.spawn or some such.
                    # reset the time counter
                # display lives and score at top of screen
                self.message_display("Score:{}".format(self.score), 0.03, 0.1, 20)
                self.message_display("Lives: {}".format(self.lives), 0.03, .85, 20)
                self.message_display("Bombs: {}".format(self.bombs), 0.03, .75, 20)

                # if out of lives - game over (see eventhandler)
                if self.lives < 1:
                    self.gameover(Board, Player1, Bullet1, Alien1, Files)

                # update the display
                pyg.display.flip()
                self.clock.tick(self.framerate)


App = Main()
App.execute()
pyg.quit()
os._exit(0)
