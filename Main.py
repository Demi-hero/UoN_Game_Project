import pygame as pyg
import os
import av_data as av
import gamedata as gd
import eventhandler as eh
import time


class Main(eh.HandleEvent):

    def __init__(self):
        # possible game states
        self.startup = True
        self.running = True
        self.paused = False
        # starting values
        self.lives = 3
        self.bombs = 1
        self.score = 0
        self.kill_score = 20
        self.penalty_score = -10
        self.difficulty = 5
        self.wavenum = 1
        self.BASE_count = 10
        self.alien_count = self.BASE_count
        # basics game needs to run
        self.white = (255, 255, 255)
        self.clock = pyg.time.Clock()
        self.starttime = 0
        self.framerate = 100
        # creating the screen and game objects
        self.all_sprites = pyg.sprite.Group()
        self.sounds = av.AudioFiles()
        self.images = av.ImageFiles()
        self.scores = av.ScoreFiles()
        self.Files = {"sounds": self.sounds, "images": self.images, "scores": self.scores}
        self.Board = gd.Background()
        self.player = gd.Player()
        self.all_sprites.add(self.player)
        self.bullets = pyg.sprite.Group()
        self.power_ups = pyg.sprite.Group()
        self.aliens = pyg.sprite.Group()
        self.smartaliens = pyg.sprite.Group()
        self.alienbullets = pyg.sprite.Group()

    def execute(self):
        # startup screen
        while self.startup:
            self.on_startup(self.Board, self.Files)
        self.starttime = time.time()

        # main game loop
        while self.running:
            # taking the player input, passing to event handler
            for event in pyg.event.get():
                self.on_event(event, self.Files, self.Board)
            self.player_movement(self.player)

            if not self.paused:
                # updating the object states
                self.Board.update()
                self.all_sprites.update()

                # spawning aliens
                self.new_alien((self.wavenum + self.difficulty))
                # spawning powerups
                if (time.time() - self.starttime) // 1 == 3 and len(self.power_ups) == 0:
                    self.new_powerup()
                elif (time.time() - self.starttime) // 1 > 15:
                    self.starttime = time.time()

                # COLLISIONS
                # check to see if a bullet hit an alien
                hits = pyg.sprite.groupcollide(self.aliens, self.bullets, False, True)
                for alien in hits:
                    alien.on_hit(self)
                # check if a player picked up a powerup
                hits = pyg.sprite.spritecollide(self.player, self.power_ups, True)
                for hit in hits:
                    hit.power_up[3]()
                # check to see if an alien hit the player
                hits = pyg.sprite.spritecollide(self.player, self.aliens, True, pyg.sprite.collide_mask)
                for hit in hits:
                    self.player_death(hit)
                # check to see if an alien bullet hit the player
                hits = pyg.sprite.spritecollide(self.player, self.alienbullets, True)
                for hit in hits:
                    self.player_death(hit)

                # once the alien_count drops below zero, new wave starts
                # alien_count gets higher and more aliens are on screen as waves increase
                if (self.alien_count <= 0) and (len(self.aliens) == 0):
                    self.wavenum += 1
                    self.message_display("Wave {}".format(self.wavenum), 0.85)
                    pyg.display.update()
                    time.sleep(1.5)
                    self.alien_count = self.BASE_count + self.wavenum*5
                    if self.wavenum % 4 == 0:
                        self.lives += 1
                        self.bombs += 1

                # removing the aliens and bullets as they leave the screen
                for alien in self.aliens:
                    if alien.rect.x < 0 - alien.ln:
                        alien.kill()
                        # penalty for if aliens get past player
                        self.score += self.penalty_score
                for bullet in self.bullets:
                    if bullet.rect.x > gd.WIDTH:
                        bullet.kill()
                for bullet in self.alienbullets:
                    if bullet.rect.x < (0 - bullet.ln):
                        bullet.kill()

                # drawing the scene
                self.Board.draw()
                self.all_sprites.draw(self.Board.screen)

                # display lives and score at top of screen
                self.message_display("Score:{}".format(self.score), 0.025, 0.1, 20)
                self.message_display("Lives: {}".format(self.lives), 0.025, .85, 20)
                self.message_display("Bombs: {}".format(self.bombs), 0.025, .75, 20)
                self.message_display("WAVE : {}".format(self.wavenum), 0.025, font_size=20)
                # if out of lives - game over (see eventhandler)
                if self.lives < 1:
                    self.gameover(self.Board, self.player, self.Files["scores"])

                # update the display
                pyg.display.flip()
                self.clock.tick(self.framerate)

pyg.init()
App = Main()
App.execute()
pyg.quit()
os._exit(0)

