import pygame as pyg
import os
import gamedata as gd
import eventhandler as eh
import time
# no realy push me
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
        self.bullets = pyg.sprite.Group()
        self.power_ups = pyg.sprite.Group()

    def new_powerup(self):
        power_up = gd.PowerUp()
        self.power_ups.add(power_up)
        gd.all_sprites.add(power_up)

    def execute(self):
        pyg.init()
        # creating the screen and game objects
        Files = gd.FileStore()
        Board = gd.Background()
        Player1 = gd.Player()
        Bullet1 = gd.Bullet()
        Alien1 = gd.Alien()
        # AlienSmart = gd.AlienSmart()
        # AlBullet = gd.AlBullet()
        Tokens = [Player1, Bullet1, Alien1]


        while self.startup:
            self.on_startup(Board, Files)
        self.starttime = time.time()
        # main game loop
        while self.running:
            # taking the player input, passing to event handler
            if (time.time() - self.starttime)//1 == 10 and len(self.power_ups) == 0:
                self.new_powerup()
                print("Power up baby")
            for event in pyg.event.get():
                self.on_event(event, Board, Tokens, Files)
            self.player_movement(gd.player)

            # updating the object states, and drawing to screen (see gamedata)
            if not self.paused:

                Board.update()
                gd.all_sprites.update()



                # check to see if a bullet hit a mob
                hits = pyg.sprite.groupcollide(gd.aliens, self.bullets, True, True)
                for hit in hits:
                    self.score += 50
                    Files.boom.play()
                    gd.expl = gd.Explosion(hit.rect.center, 'lg')
                    gd.all_sprites.add(gd.expl)
                    gd.new_alien()

                hits = pyg.sprite.spritecollide(gd.player, self.power_ups, True)
                for hit in hits:
                    print("Power up collected")

                # check to see if a mob hit the player
                hits = pyg.sprite.spritecollide(gd.player, gd.aliens, True, pyg.sprite.collide_circle)
                for hit in hits:
                    print (hit)
                    self.lives -= 1
                    Files.boom.play()
                    gd.expl = gd.Explosion(hit.rect.center, 'sm')
                    gd.all_sprites.add(gd.expl)
                    gd.new_alien()
                    gd.player.hide()
                for alien in gd.aliens:
                    if alien.rect.x < 0 - alien.ln:
                        gd.aliens.remove(alien)
                        self.score -= 10
                        gd.new_alien()

                Board.draw()
                gd.all_sprites.draw(gd.Background.screen)

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
