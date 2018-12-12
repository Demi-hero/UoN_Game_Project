import pygame as pyg
import os
import gamedata
import time
import csv
from random import randint

class HandleEvent():

    # startup screen and logic
    def on_startup(self, background, files):
        background.draw()
        background.update()
        # self.message_display("Highscores :",xloc=.35)
        # self.message_display(" Lore :", xloc=.65)
        self.message_display("Movement", yloc=.93, xloc=.13, font_size=25)
        self.message_display("Shoot", yloc=.93, xloc=.87, font_size=25)
        background.screen.blit(files["images"].title, (221, 0))
        background.screen.blit(files["images"].arrows, (50, 375))
        # gamedata.background.screen.blit(Game_Data.startup.h, (425, 228))
        # gamedata.background.screen.blit(Game_Data.startup.l, (675, 228))
        background.screen.blit(files["images"].space, (760, 426))
        self.message_display("-Press Shoot to Start-", .8, font_size=35)
        pyg.display.flip()
        while self.startup:
            for event in pyg.event.get():
                self.on_event(event, files=files)
            pyg.display.flip()

    # pause screen messages
    def on_pause(self, minimised=0):
        if not self.paused:
            self.paused = True
            for alien in self.aliens:
                alien.vx = 0
                alien.firing_solution = 0
            for bullet in self.alienbullets:
                bullet.vx = 0
            self.message_display("GAME PAUSED", .30)
            self.message_display("Press p to unpause")
            self.message_display("Press q to quit", .65)
            pyg.display.update()
        elif not minimised:
            for alien in self.aliens:
                alien.vx = -2
                alien.firing_solution = 1
            for bullet in self.alienbullets:
                bullet.vx = -10
            self.paused = False

    # game over screen and logic
    def gameover(self, board, player, files):
        # display high score messages
        if self.scorboard_check(files):
            self.on_new_highscore(board, player, files)
        else:
            self.message_display("Your Score: {}".format(self.score), .75)
        self.highscore_display(board, files)
        self.message_display("Press any key to try again", .85)
        pyg.display.update()
        time.sleep(1.5)

        while True:
            for event in pyg.event.get():
                if event.type == pyg.QUIT:
                    pyg.quit()
                    os._exit(0)
                elif event.type == pyg.KEYDOWN:
                    # if key pressed, re-initialises everything and breaks from loop
                    for sprite in self.all_sprites:
                        sprite.kill()
                    self.__init__()
                    return

    def game_over_display(self, board):
        # the text we want on every game over page
        board.draw()
        board.update()
        self.message_display("Game Over", yloc=0.1, font_size=35)

    # code for creating messages
    def text_objects(self, text, font):
        textsurface = font.render(text, True, pyg.Color("white"))
        return textsurface, textsurface.get_rect()

    def message_display(self, words, yloc=.45, xloc=.5, font_size=50):
        text = pyg.font.Font('freesansbold.ttf', font_size)
        textsurf, textrect = self.text_objects(words, text)
        textrect.center = (gamedata.WIDTH * xloc), (gamedata.HEIGHT * yloc)
        gamedata.Background.screen.blit(textsurf, textrect)

    # methods for the high score handling
    def highscore_display(self, board, files):
        pos = 0.2
        self.game_over_display(board)
        self.message_display("HIGH SCORES", pos, font_size=45)
        pos += 0.05
        for values in files.scores:
            pos += 0.05
            self.message_display("{} : {}".format(values[0], values[1]), pos, font_size=20)

    def on_new_highscore(self, board, player, files):
        player.altering_name = True
        files.high_score = self.score
        while player.altering_name:
            self.game_over_display(board)
            self.message_display("YOU MADE THE SCORE BOARD WITH: {}!".format(self.score), .45, font_size=35)
            self.message_display("PLEASE ENTER YOUR NAME", .55, .5, font_size=35)
            self.message_display("Player Name: {}".format(player.player_name), .65, font_size=35)

            for event in pyg.event.get():
                if event.type == pyg.KEYDOWN:
                    if event.unicode.isalpha():
                        player.update_name(event.unicode)
                    elif event.key == pyg.K_BACKSPACE:
                        player.update_name("", 1)
                    elif event.key == pyg.K_RETURN:
                        files.scoreboard = [player.player_name, self.score]
                        player.altering_name = False
                elif event.type == pyg.QUIT:
                    pyg.quit()
                    quit()
            pyg.display.flip()
        files.update_scores()

    def scorboard_check(self, Files):
        for lists in Files.scores:
            if self.score > int(lists[1]):
                return True
        return False

    # this runs for every event and calls the relevant method - mostly for checking player input
    def on_event(self, event, files="", board = ""):
        # breaks out of the main game loop if QUIT event occurs (closing window), cleanup occurs after
        if event.type == pyg.QUIT:
                self.on_exit()
        # checks for when keys are pressed
        elif event.type == pyg.KEYDOWN:
                self.on_key_down(event, files, board)
        elif event.type == pyg.ACTIVEEVENT:
            if event.state == 6:
                self.on_pause()

    def on_exit(self):
        self.startup = False
        self.running = False

    # calculating the player movement direction based on arrow keys held down
    def player_movement(self, Player):
        keystate = pyg.key.get_pressed()
        x_dir = keystate[pyg.K_RIGHT] - keystate[pyg.K_LEFT]
        y_dir = keystate[pyg.K_DOWN] - keystate[pyg.K_UP]
        Player.move(x_dir, y_dir)

    def on_key_down(self, event, files, board):
        if (event.key == pyg.K_SPACE) and not self.paused:
            files['sounds'].pewpew.play()
            if self.startup:
                # if on startup, spacebar starts the game
                self.startup = False
            else:
                # spacebar triggers firing sequence - takes gun position from player, passes to bullet fire method
                bullet = gamedata.Bullet()
                bullet.rect.x = self.player.rect.x + self.player.ln//2
                bullet.rect.y = self.player.rect.y + self.player.ht//2
                self.all_sprites.add(bullet)
                self.bullets.add(bullet)

        # p opens the pause screen, and q quits if on the pause screen
        elif (event.key == pyg.K_p) and not self.startup:
            self.on_pause()
        elif event.key == pyg.K_q:
            self.on_exit()
        # b drops a bomb
        elif event.key == pyg.K_b:
            self.on_bomb(board, files)

    # logic for bomb power-up
    def on_bomb(self, board, files):
        if self.bombs > 0 and not self.paused:
            files['sounds'].ult.play()
            self.score += 500
            self.alien_count -= len(self.aliens)
            self.purge_aliens()
            pyg.display.update()
            self.bombs -= 1

    # on player death updates life count, creates explosion, and clears screen
    def player_death(self, hit):
        self.lives -= 1
        self.sounds.boom.play()
        expl = gamedata.Explosion(hit.rect.center, 'lg')
        self.all_sprites.add(expl)
        self.player.hide()
        for bullet in self.bullets:
            bullet.kill()
        # adds back to the kill count the aliens that were alive, before clearing screen
        self.alien_count += len(self.aliens)
        self.purge_aliens(player_death=1)

    # spawns aliens, rate increases as player completes waves
    def new_alien(self, amount=1):
        if (len(self.aliens) <= amount) and (self.alien_count > 0):
            self.alien_count -= 1
            # spawns a smart alien if one doesn't exist
            if len(self.smartaliens) == 0:
                smartalien = gamedata.SmartAlien(self)
                self.all_sprites.add(smartalien)
                self.aliens.add(smartalien)
                self.smartaliens.add(smartalien)
            # %25 chance of spawning a shield alien
            elif randint(1,4) == 1:
                shieldalien = gamedata.ShieldAlien(self)
                self.spawn_check(shieldalien)
            # otherwise spawns a normal alien
            else:
                alien = gamedata.Alien(self)
                self.spawn_check(alien)

    def spawn_check(self, alien):
        alien.collide(self.aliens)
        self.all_sprites.add(alien)
        self.aliens.add(alien)

    # spawns powerups
    def new_powerup(self):
        power_up = gamedata.PowerUp(self)
        self.power_ups.add(power_up)
        self.all_sprites.add(power_up)

    def purge_aliens(self,player_death=0):
        for alien in self.aliens:
            if not player_death:
                self.expl = gamedata.Explosion(alien.rect.center, 'sm')
                self.all_sprites.add(self.expl)
            alien.kill()
        for albull in self.alienbullets:
            albull.kill()
