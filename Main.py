import pygame as pyg
import os
import gamedata as gd
import eventhandler as eh

class Main(eh.HandleEvent):

    def __init__(self):
        self.startup = True
        self.running = True
        self.paused = False
        self.lives = 3
        self.bombs = 1
        self.score = 0
        self.white = (255,255,255)
        self.clock = pyg.time.Clock()
        self.framerate = 100

    def execute(self):
        pyg.init()
        # creating the screen and game objects
        Files = gd.FileStore()
        Board = gd.Background()
        Player1 = gd.Player()
        Bullet1 = gd.Bullet()
        Alien1 = gd.Alien()
        AlienSmart = gd.AlienSmart()
        AlBullet = gd.AlBullet()
        power_up = gd.PowerUp(self)
        Tokens = [Player1, Bullet1, Alien1, AlienSmart, AlBullet]

        while self.startup:
            self.on_startup(Board, Files)

        # main game loop
        while self.running:
            # taking the player input, passing to event handler
            for event in pyg.event.get():
                self.on_event(event, Board, Tokens, Files)
            self.player_movement(Player1)

            # updating the object states, and drawing to screen (see gamedata)
            if not self.paused:
                Board.draw()
                Player1.draw()
                power_up.spawn(Player1)
                Bullet1.draw()
                Alien1.draw()
                AlienSmart.draw()
                AlBullet.draw()

                Board.update()
                Bullet1.update()
                # passes main (self) to alien update and detect_collision to update score and lives
                Alien1.update(AlBullet, self)
                AlienSmart.update(Player1, AlBullet, self)
                AlBullet.update()

                # detecting collisions between aliens and bullets, and aliens and player
                Alien1.detect_collisions(Tokens, self)
                AlienSmart.detect_collisions(Tokens, self)
                AlBullet.detect_collisions(Tokens, self)

                # display lives and score at top of screen
                self.message_display("Score:{}".format(self.score), 0.03, 0.1, 20)
                self.message_display("Lives: {}".format(self.lives), 0.03, .85, 20)
                self.message_display("Bombs: {}".format(self.bombs), 0.03, .75, 20)

                # if out of lives - game over (see eventhandler)
                if self.lives < 1:
                    self.gameover(Board, Tokens, Files)

                # update the display
                pyg.display.flip()
                self.clock.tick(self.framerate)

App = Main()
App.execute()
pyg.quit()
os._exit(0)
