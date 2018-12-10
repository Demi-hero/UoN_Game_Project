import pygame as pyg
import os
import gamedata as gd
import eventhandler as eh
import time
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
        self.starttime = 0
        self.framerate = 100
        self.wavenum = 1
        # creating the screen and game objects
        self.all_sprites = pyg.sprite.Group()
        self.Files = gd.FileStore()
        self.Board = gd.Background()
        self.player = gd.Player()
        self.all_sprites.add(self.player)
        self.bullets = pyg.sprite.Group()
        self.power_ups = pyg.sprite.Group()
        self.aliens = pyg.sprite.Group()
        self.alienbullets = pyg.sprite.Group()


    def new_powerup(self):
        power_up = gd.PowerUp(self)
        self.power_ups.add(power_up)
        self.all_sprites.add(power_up)

    def execute(self):


        self.new_alien(self.wavenum)

        while self.startup:
            self.on_startup(self.Board, self.Files)
        self.starttime = time.time()
        # main game loop
        while self.running:
            # taking the player input, passing to event handler

            for event in pyg.event.get():
                self.on_event(event, self.Files, self.Board)
            self.player_movement(self.player)

            # updating the object states, and drawing to screen (see gamedata)
            if not self.paused:

                if (time.time() - self.starttime) // 1 == 3 and len(self.power_ups) == 0:
                    self.new_powerup()
                elif (time.time() - self.starttime) // 1 > 15:
                    self.starttime = time.time()
                self.Board.update()
                self.all_sprites.update()

                # check to see if a bullet hit a mob
                hits = pyg.sprite.groupcollide(self.aliens, self.bullets, True, True)
                for hit in hits:
                    self.score += 50
                    self.Files.boom.play()
                    self.expl = gd.Explosion(hit.rect.center, 'lg')
                    self.all_sprites.add(self.expl)
                    self.new_alien(-6)

                hits = pyg.sprite.spritecollide(self.player, self.power_ups, True)
                for hit in hits:
                    hit.power_up[3]()
                    print("Power up collected")

                # check to see if a mob hit the player
                hits = pyg.sprite.spritecollide(self.player, self.aliens, True, pyg.sprite.collide_circle)
                for hit in hits:
                    self.player_death(hit)


                for alien in self.aliens:
                    if alien.rect.x < 0 - alien.ln:
                        self.aliens.remove(alien)
                        self.score -= 10
                        self.new_alien( -6)
                for bullet in self.bullets:
                    if bullet.rect.x > gd.WIDTH:
                        bullet.kill()
                for bullet in self.alienbullets:
                    if bullet.rect.x < (0 - bullet.ln):
                        bullet.kill()
                hits = pyg.sprite.spritecollide(self.player, self.alienbullets, True)
                for hit in hits:
                    self.player_death(hit)



                self.Board.draw()
                self.all_sprites.draw(self.Board.screen)

                # display lives and score at top of screen
                self.message_display("Score:{}".format(self.score), 0.03, 0.1, 20)
                self.message_display("Lives: {}".format(self.lives), 0.03, .85, 20)
                self.message_display("Bombs: {}".format(self.bombs), 0.03, .75, 20)
                self.message_display("WAVE : {}".format(self.wavenum), 0.05)

                # if out of lives - game over (see eventhandler)
                if self.lives < 1:
                    self.gameover(self.Board, self.player, self.Files)

                # update the display
                pyg.display.flip()
                self.clock.tick(self.framerate)

pyg.init()
App = Main()
App.execute()
pyg.quit()
os._exit(0)
