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
        self.bullets = pyg.sprite.Group()

    def execute(self):
        pyg.init()
        # creating the screen and game objects
        Files = gd.FileStore()
        Board = gd.Background()
        Player1 = gd.Player()
        Bullet1 = gd.Bullet()
        Alien1 = gd.Alien()
        AlienSmart = gd.AlienSmart()
        # AlBullet = gd.AlBullet()
        power_up = gd.PowerUp(self)
        Tokens = [Player1, Bullet1, Alien1, AlienSmart]


        while self.startup:
            self.on_startup(Board, Files)

        # main game loop
        while self.running:
            # taking the player input, passing to event handler
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
                    print(hit)
                    gd.new_alien()

                # check to see if a mob hit the player
                hits = pyg.sprite.spritecollide(gd.player, gd.aliens, True, pyg.sprite.collide_circle)
                for hit in hits:
                    print (hit)
                    self.lives -= 1
                    # gd.player.death()
                    # player.shield -= hit.radius * 2
#                   expl = gd.Explosion(hit.rect.center, 'sm')
#                   gd.all_sprites.add(expl)
                    gd.new_alien()
#        if player.shield <= 0:
#            running = False
                for alien in gd.aliens:
                    if alien.rect.x < 0 - alien.ln:
                        gd.aliens.remove(alien)
                        self.score - 10
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
