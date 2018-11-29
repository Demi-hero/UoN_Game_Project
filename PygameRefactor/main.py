import pygame as pyg
import os
from gamedata import *
from eventhandler import *

class Main(HandleEvent):

    def __init__(self):
        self.running = True
        self.paused = False
        self.lives = 3
        self.score = 0
        self.clock = pyg.time.Clock()
        self.framerate = 100

    def execute(self):
        pyg.init()
        # creating the screen and game objects
        Board = Background()
        Player1 = Player()
        Bullet1 = Bullet()
        Alien1 = Alien()

        # main game loop
        while self.running:
            # taking the player input, passing to event handler
            for event in pyg.event.get():
                self.on_event(event, Player1, Bullet1)
            self.player_movement(Player1)

            # updating the object states, and drawing to screen (see gamedata)
            if not self.paused:
                Board.update()
                Player1.update()
                Bullet1.update()
                # passes main (self) to alien update and detect_collision to update score and lives
                Alien1.update(self)
                # detecting collisions between aliens and bullets, and aliens and player
                Alien1.detect_collisions(Player1, Bullet1, self)

                # display lives and score at top of screen
                self.message_display("Score:{}".format(self.score), 0.03, 0.1, 20)
                self.message_display("Lives: {}".format(self.lives), 0.03, .85, 20)

                # if out of lives - game over (see eventhandler)
                if self.lives < 1:
                    self.gameover(Player1, Bullet1, Alien1)

                # update the display
                print(Bullet1.alive_bullets)
                pyg.display.flip()
                self.clock.tick(self.framerate)

App = Main()
App.execute()
pyg.quit()
os._exit(0)
