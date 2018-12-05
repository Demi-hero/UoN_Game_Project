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
        Board = gd.Background()
        Files = gd.FileStore()
        all_sprites = pyg.sprite.Group()
        Player1 = gd.Player()
        Bullet1 = pyg.sprite.Group()
        Alien1 = pyg.sprite.Group()
        AlienSmart = pyg.sprite.Group()
        AlBullet = pyg.sprite.Group()
        power_up = pyg.sprite.Sprite
        # all_sprites.add(power_up)

        while self.startup:
            self.on_startup(Board, Files)

        # main game loop
        while self.running:
            # taking the player input, passing to event handler
            for event in pyg.event.get():
                self.on_event(event, Board, Files)

            # updating the object states, and drawing to screen (see gamedata)
            if not self.paused:
                self.player_movement(Player1)
                all_sprites.update()
                # power_up.spawn(Player1)
                # Board.update()
                # Bullet1.update()
                # passes main (self) to alien update and detect_collision to update score and lives
                # Alien1.update(AlBullet, self)
                # AlienSmart.update(Player1, AlBullet, self)
                # AlBullet.update()

                # detecting collisions between aliens and bullets, and aliens and player
                hits = pyg.sprite.groupcollide(Alien1, Bullet1, True, True)
                for hit in hits:
                    score += 20
                    # eploud goes here
                    self.on_dead_alien()

                hits = pyg.sprite.spritecollide(Player1, Alien1, False, pyg.sprite.collide_circle)
                for hit in hits:
                    self.on_dead_alien()
                # display lives and score at top of screen
                self.message_display("Score:{}".format(self.score), 0.03, 0.1, 20)
                self.message_display("Lives: {}".format(self.lives), 0.03, .85, 20)
                self.message_display("Bombs: {}".format(self.bombs), 0.03, .75, 20)

                # if out of lives - game over (see eventhandler)
                if self.lives < 1:
                    self.gameover(Board, Tokens, Files)

                all_sprites.draw(Board.screen)
                # update the display
                pyg.display.flip()
                self.clock.tick(self.framerate)
                self.point_threshold()

App = Main()
App.execute()
pyg.quit()
os._exit(0)
