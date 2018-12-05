import pygame as pyg
import os
import gamedata as gd
import eventhandler as eh

class Main(eh.HandleEvent):

    def __init__(self):
        pyg.init()
        self.startup = True
        self.running = True
        self.paused = False
        self.lives = 3
        self.bombs = 1
        self.score = 0
        self.white = (255,255,255)
        self.clock = pyg.time.Clock()
        self.framerate = 100
        self.all_sprites = pyg.sprite.Group()
        self.Player1 = gd.Player()
        self.Board = gd.Background()
        self.Files = gd.FileStore()
        self.Bullet1 = pyg.sprite.Group()
        self.Alien1 = pyg.sprite.Group()
        self.AlienSmart = pyg.sprite.Group()
        self.AlBullet = pyg.sprite.Group()
        self.power_up = pyg.sprite.Sprite

    def execute(self):
        # creating the screen and game objects

        # all_sprites.add(power_up)

        while self.startup:
            self.on_startup(self.Board, self.Files)

        self.Board.screen.fill((0,0,0))
        # main game loop
        while self.running:
            # taking the player input, passing to event handler
            for event in pyg.event.get():
                self.on_event(event, self.Board, self.Files)

            # updating the object states, and drawing to screen (see gamedata)
            if not self.paused:
                self.player_movement(self.Player1)
                self.all_sprites.update()
                # power_up.spawn(Player1)
                # Board.update()
                # Bullet1.update()
                # passes main (self) to alien update and detect_collision to update score and lives
                # Alien1.update(AlBullet, self)
                # AlienSmart.update(Player1, AlBullet, self)
                # AlBullet.update()

                # detecting collisions between aliens and bullets, and aliens and player
                hits = pyg.sprite.groupcollide(self.Alien1, self.Bullet1, True, True)
                for hit in hits:
                    self.score += 20
                    # eploud goes here
                    self.on_dead_alien()

                hits = pyg.sprite.spritecollide(self.Player1, self.Alien1, False, pyg.sprite.collide_circle)
                for hit in hits:
                    self.on_dead_alien()
                # display lives and score at top of screen
                self.message_display("Score:{}".format(self.score), 0.03, 0.1, 20)
                self.message_display("Lives: {}".format(self.lives), 0.03, .85, 20)
                self.message_display("Bombs: {}".format(self.bombs), 0.03, .75, 20)

                # if out of lives - game over (see eventhandler)
                if self.lives < 1:
                    self.gameover(self.Board, self.Files)

                self.all_sprites.draw(self.Board.screen)
                # update the display
                pyg.display.flip()
                self.clock.tick(self.framerate)
                self.point_threshold()

App = Main()
App.execute()
pyg.quit()
os._exit(0)
