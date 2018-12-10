import pygame as pyg
import os
import gamedata
import time
import csv
# push me please
class HandleEvent():

    def on_startup(self, background, files):
        background.draw()
        background.update()
        # self.message_display("Highscores :",xloc=.35)
        # self.message_display(" Lore :", xloc=.65)
        self.message_display("Movement", yloc=.57, xloc=.26)
        self.message_display("Shoot", yloc=.65, xloc=.7)
        background.screen.blit(files.title, (221, 0))
        background.screen.blit(files.arrows, (160, 320))
        # gamedata.background.screen.blit(Game_Data.startup.h, (425, 228))
        # gamedata.background.screen.blit(Game_Data.startup.l, (675, 228))
        background.screen.blit(files.space, (591, 375))
        self.message_display("Press Shoot to Start", .9, font_size=35)
        pyg.display.flip()
        while self.startup:
            for event in pyg.event.get():
                self.on_event(event, files=files)
            pyg.display.flip()

    # calculating the player movement direction based on arrow keys held down
    def player_movement(self, Player):
        keystate = pyg.key.get_pressed()
        x_dir = keystate[pyg.K_RIGHT] - keystate[pyg.K_LEFT]
        y_dir = keystate[pyg.K_DOWN] - keystate[pyg.K_UP]
        Player.move(x_dir, y_dir)

    # this runs for every event and calls the relevant method
    def on_event(self, event, files="", board = ""):
        # breaks out of the main game loop if QUIT event occurs (closing window), cleanup occurs after
        if event.type == pyg.QUIT:
                self.on_exit()
        # checks for when keys are pressed
        elif event.type == pyg.KEYDOWN:
                self.on_key_down(event, files, board)

    def on_exit(self):
        self.startup = False
        self.running = False

    def on_key_down(self, event, files, board):
        # spacebar triggers firing sequence - takes gun position from player, passes to bullet fire method
        if event.key == pyg.K_SPACE:
            files.pewpew.play()
            if self.startup:
                self.startup = False
            else:
                bullet = gamedata.Bullet()
                bullet.rect.x = gamedata.player.rect.x + gamedata.player.ln//2
                bullet.rect.y = gamedata.player.rect.y + gamedata.player.ht//2
                gamedata.all_sprites.add(bullet)
                self.bullets.add(bullet)
        # p opens the pause screen, and q quits if on the pause screen
        elif event.key == pyg.K_p:
            self.on_pause()
        elif event.key == pyg.K_q:
            if self.paused:
                self.on_exit()
        elif event.key == pyg.K_b:
            self.on_bomb(board, files)

    def on_bomb(self, board, files):
        if self.bombs > 0:
            counter = 0
            files.ult.play()
            self.update_score(1000)
            board.screen.fill(self.white)
            for alien in gamedata.aliens:
                alien.kill()
                counter += 1
            pyg.display.update()
            self.bombs -= 1
            for i in range(counter):
                gamedata.new_alien()


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
                    for sprite in gamedata.all_sprites:
                        sprite.kill()
                    gamedata.player = gamedata.Player()
                    gamedata.all_sprites.add(gamedata.player)
                    for i in range(8):
                        gamedata.new_alien()
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

    def message_display(self, text, yloc=.45, xloc=.5, font_size=50):
        largetext = pyg.font.Font('freesansbold.ttf', font_size)
        textsurf, textrect = self.text_objects(text, largetext)
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
