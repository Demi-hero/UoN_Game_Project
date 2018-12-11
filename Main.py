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
        self.difficulty = 7
        self.wavenum = 1
        self.kill_count = 0
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
        self.alienbullets = pyg.sprite.Group()


    def execute(self):
        # spawning aliens
        self.new_alien((self.wavenum + self.difficulty))

        # startup screen
        while self.startup:
            self.on_startup(self.Board, self.Files)
        self.starttime = time.time()

        # main game loop
        while self.running:

            # updating the object states
            self.Board.update()
            self.all_sprites.update()

            # taking the player input, passing to event handler
            for event in pyg.event.get():
                self.on_event(event, self.Files, self.Board)
            self.player_movement(self.player)

            if not self.paused:
                # spawning powerups
                if (time.time() - self.starttime) // 1 == 3 and len(self.power_ups) == 0:
                    self.new_powerup()
                elif (time.time() - self.starttime) // 1 > 15:
                    self.starttime = time.time()



                # COLLISIONS
                # check to see if a bullet hit an alien
                hits = pyg.sprite.groupcollide(self.aliens, self.bullets, True, True)
                for hit in hits:

                    self.score += self.kill_score
                    self.kill_count += 1
                    self.sounds.boom.play()
                    self.expl = gd.Explosion(hit.rect.center, 'lg')
                    self.all_sprites.add(self.expl)
                    self.new_alien()
                # check if a player picked up a powerup
                hits = pyg.sprite.spritecollide(self.player, self.power_ups, True)
                for hit in hits:
                    hit.power_up[3]()
                # check to see if an alien hit the player
                hits = pyg.sprite.spritecollide(self.player, self.aliens, True, pyg.sprite.collide_circle)
                for hit in hits:
                    self.player_death(hit)
                # check to see if an alien bullet hit the player
                hits = pyg.sprite.spritecollide(self.player, self.alienbullets, True)
                for hit in hits:
                    self.player_death(hit)

                if self.kill_count >= (self.difficulty + self.wavenum):
                    self.kill_count -= (self.difficulty + self.wavenum)
                    self.wavenum += 1
                    if self.wavenum % 4 == 0:
                        self.lives += 1
                        self.bombs += 1
                    self.purge_aliens()
                    self.new_alien(self.wavenum + self.difficulty)
                    # kill the bad guys
                    # make more bad guys

                # removing the aliens and bullets as they leave the screen
                for alien in self.aliens:
                    if alien.rect.x < 0 - alien.ln:
                        self.aliens.remove(alien)
                        # penalty for if aliens get past player
                        self.score += self.penalty_score
                        self.new_alien()
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
