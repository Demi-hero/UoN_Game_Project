import pygame as pyg
import os
import gamedata
import time

class HandleEvent():

    # calculating the player movement direction based on arrow keys held down
    def player_movement(self, Player):
        keystate = pyg.key.get_pressed()
        x_dir = keystate[pyg.K_RIGHT] - keystate[pyg.K_LEFT]
        y_dir = keystate[pyg.K_DOWN] - keystate[pyg.K_UP]
        Player.move(x_dir, y_dir)

    # this runs for every event and calls the relevant method
    def on_event(self, event, Player, Bullet):
        # breaks out of the main game loop if QUIT event occurs (closing window), cleanup occurs after
        if event.type == pyg.QUIT:
                self.on_exit()
        # checks for when keys are pressed
        elif event.type == pyg.KEYDOWN:
                self.on_key_down(event, Player, Bullet)

    def on_exit(self):
        self.running = False

    def on_key_down(self, event, Player, Bullet):
        # spacebar triggers firing sequence - takes gun position from player, passes to bullet fire method
        if event.key == pyg.K_SPACE:
            gun_pos = Player.get_gun_location()
            Bullet.fire(gun_pos)
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
        # display messages
        self.message_display("Game Over")
        self.message_display("Press any key to try again", .65)
        pyg.display.update()
        # brief pause so player doesn't accidentally restart
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

    # code for creating messages
    def text_objects(self, text, font):
        textsurface = font.render(text, True, pyg.Color("white"))
        return textsurface, textsurface.get_rect()

    def message_display(self, text, yloc=.45, xloc=.5, font_size=50):
        largetext = pyg.font.Font('freesansbold.ttf', font_size)
        textsurf, textrect = self.text_objects(text, largetext)
        textrect.center = (gamedata.WIDTH * xloc), (gamedata.HEIGHT * yloc)
        gamedata.Background.screen.blit(textsurf, textrect)
