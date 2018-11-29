import pygame as pyg
import os
import gamedata
import time
import csv

class HandleEvent():

    # calculating the player movement direction based on arrow keys held down
    def player_movement(self, Player):
        keystate = pyg.key.get_pressed()
        x_dir = keystate[pyg.K_RIGHT] - keystate[pyg.K_LEFT]
        y_dir = keystate[pyg.K_DOWN] - keystate[pyg.K_UP]
        Player.move(x_dir, y_dir)

    # this runs for every event and calls the relevant method
    def on_event(self, event, player="", bullet="", files=''):
        # breaks out of the main game loop if QUIT event occurs (closing window), cleanup occurs after
        if event.type == pyg.QUIT:
                self.on_exit()
        # checks for when keys are pressed
        elif event.type == pyg.KEYDOWN:
                self.on_key_down(event, player, bullet, files)

    def on_exit(self):
        self.running = False

    def on_key_down(self, event, player, bullet, files):
        # spacebar triggers firing sequence - takes gun position from player, passes to bullet fire method
        if event.key == pyg.K_SPACE:
            files.pewpew.play()
            if self.startup:
                self.startup = False
            else:
                gun_pos = player.get_gun_location()
                bullet.fire(gun_pos)
        # p opens the pause screen, and q quits if on the pause screen
        elif event.key == pyg.K_p:
            self.on_pause()
        elif event.key == pyg.K_q:
            if self.paused:
                self.on_exit()

    # update score and lives
    def update_score(self, points):
        self.score += points
    def update_lives(self, change):
        self.lives += change

    # pause screen messages
    def on_pause(self, minimised=0):
        if not self.paused:
            self.paused = True
            self.message_display("GAME PAUSED", .30)
            self.message_display("Press p to unpause")
            self.message_display("Press q to quit", .65)
            pyg.display.update()
        elif not minimised:
            self.paused = False

    def gameover(self, Player, Bullet, Alien):
        # display high score messages
        if self.scorboard_check():
            self.on_new_highscore()
        else:
            self.message_display("Your Score: {}".format(self.score), .75)
        self.highscore_display()
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
                    Player.__init__()
                    Bullet.__init__()
                    Alien.__init__()
                    self.__init__()
                    return

    def game_over_display(self):
        # the text we want on every game over page
        self.Board.update()
        self.message_display("Game Over", yloc=0.1, font_size=35)

    # code for creating messages
    def text_objects(self, text, font):
        textsurface = font.render(text, True, pyg.Color("white"))
        return textsurface, textsurface.get_rect()

    def message_display(self, text, yloc=.45, xloc=.5, font_size=50):
        largetext = pyg.font.Font('freesansbold.ttf', font_size)
        textsurf, textrect = self.text_objects(text, largetext)
        textrect.center = (gamedata.WIDTH * xloc), (gamedata.HEIGHT * yloc)
        gamedata.Background.screen.blit(textsurf, textrect)

    # methods for the high score handling

    def highscore_display(self):
        pos = 0.2
        self.game_over_display()
        self.message_display("HIGH SCORES", pos, font_size=45)
        pos += 0.05
        for values in self.Files.scores:
            pos += 0.05
            self.message_display("{} : {}".format(values[0], values[1]), pos, font_size=20)

    def on_new_highscore(self):
        self.Player1.altering_name = True
        self.Files.high_score = self.score
        while self.Player1.altering_name:
            self.game_over_display()
            self.message_display("YOU MADE THE SCORE BOARD WITH: {}!".format(self.score), .45, font_size=35)
            self.message_display("PLEASE ENTER YOUR NAME", .55, .5, font_size=35)
            self.message_display("Player Name: {}".format(self.Player1.player_name), .65, font_size=35)

            for event in pyg.event.get():
                if event.type == pyg.KEYDOWN:
                    if event.unicode.isalpha():
                        self. Player1.update_name(event.unicode)
                    elif event.key == pyg.K_BACKSPACE:
                        self.Player1.update_name("", 1)
                    elif event.key == pyg.K_RETURN:
                        self.Files.scoreboard = [self.Player1.player_name, self.score]
                        self.Player1.altering_name = False
                elif event.type == pyg.QUIT:
                    pyg.quit()
                    quit()
            pyg.display.flip()
        self.Files.update_scores()

    def scorboard_check(self):
        for lists in self.Files.scores:
            if self.score > int(lists[1]):
                return True
        return False
