import pygame as pyg
import os
from eventhandler import *
from random import randint

# constants for the screen
WIDTH = 960
HEIGHT = 540
BORDER = 10

# Background object contains the display, and draws and updates the animated background
class Background:
    screen = pyg.display.set_mode((WIDTH, HEIGHT))

    def __init__(self):
        self.white = (255,255,255)
        # loading the background image - two copies, to allow it to scroll
        self.bg1 = pyg.image.load(os.path.join("images", "background.jpg"))
        self.bg2 = pyg.image.load(os.path.join("images", "background.jpg"))
        self.bg1_x = 0
        self.bg2_x = self.bg1.get_width()

    def update(self):
        self.screen.fill(self.white)
        self.screen.blit(self.bg1, (self.bg1_x, 0))
        self.screen.blit(self.bg2, (self.bg2_x, 0))
        # updating the background positions so it scrolls
        self.bg1_x -= 1
        self.bg2_x -= 1
        if self.bg1_x <= -(self.bg1.get_width()):
                self.bg1_x = self.bg2_x + self.bg2.get_width()
        if self.bg2_x <= -(self.bg2.get_width()):
                self.bg2_x = self.bg1_x + self.bg1.get_width()

class Player:
    # loading the player sprite and getting it's dimensions
    sprite = pyg.image.load(os.path.join("images", "hero_side.png"))
    ln = sprite.get_width()
    ht = sprite.get_height()
    # loading the images for the sprite with animated thrusters
    animated_sprite = [pyg.image.load(os.path.join("images", "hero_side1.png")),
               pyg.image.load(os.path.join("images", "hero_side2.png")),
               pyg.image.load(os.path.join("images", "hero_side3.png"))]
    # this is the x-coordinate offset of the animated image, to account for it being longer due to the thrusters
    animation_offset_x = ln - animated_sprite[0].get_width()

    def __init__(self):
        # initialising position on screen, speed and hitbox
        self.x = BORDER
        self.y = HEIGHT//2 - self.ht
        self.speed = 4
        self.hitbox = pyg.Rect(self.x, self.y, self.ln, self.ht)
        # animation loop - as it increments up, different images of the sprite are drawn, resulting in animation
        self.animation_loop = 0
        # x-axis velocity, used to determine whether to animate thrusters
        self.x_vel = 0

    def get_gun_location(self):
        # returns the gun position to the event handler, who passes it to bullet fire method
        x_gun = self.x + self.ln//2
        y_gun = self.y + self.ht//2
        return [x_gun, y_gun]

    def get_hitbox(self):
        return self.hitbox

    def on_hit(self, Alien, Bullet, Main):
        # when player is hit, re-initialises the objects to clear the screen
        self.__init__()
        Alien.__init__()
        Bullet.__init__()
        # updates number of lives
        Main.update_lives(-1)

    def move(self, x_dir, y_dir):
        # takes the direction of movement from the event handler, multiplies by speed
        if (x_dir != 0) and (y_dir != 0):
            # this modifies the speed if moving diagonally
            velocity = int(self.speed * 0.8)
        else:
            velocity = self.speed
        # this step is here for animation purposes - it flags whether to animate thrusters
        self.x_vel = x_dir
        x_new = self.x + (x_dir * velocity)
        y_new = self.y + (y_dir * velocity)
        # checks if the new positions are in the play area, and updates if they are
        if (x_new > BORDER) and (x_new < (WIDTH//2)):
            self.x = x_new
        if (y_new > BORDER) and (y_new < HEIGHT-BORDER-self.ht):
            self.y = y_new

    def update(self):
        # moves hitbox to current position and draws self on screen
        self.hitbox = pyg.Rect(self.x, self.y, self.ln, self.ht)
        # if player moving backwards, draws ship without thrusters
        if self.x_vel < 0:
            Background.screen.blit(self.sprite, (self.x, self.y))
        # otherwise draws animated ship, and increments through animation loop
        else:
            Background.screen.blit(self.animated_sprite[self.animation_loop//3], (self.x+self.animation_offset_x, self.y))
            self.animation_loop += 1
            # reseting animation loop as only has three images to cycle through
            if self.animation_loop >= 9:
                self.animation_loop = 0

class Bullet:
    # loading the bullet sprite and getting it's dimensions
    sprite = pyg.image.load(os.path.join("images", "bullet.png"))
    ln = sprite.get_width()
    ht = sprite.get_height()

    def __init__(self):
        # bullet velocity
        self.vx = 15
        # a list of lists - each entry is the [x,y] co-ordinates of a 'live' bullet
        self.alive_bullets = []

    def get_alive_bullets(self):
        return self.alive_bullets

    def get_size(self):
        # returns its dimensions so the alien detect_collisions method can create hitboxes
        return [self.ln, self.ht]

    def fire(self, gun_pos):
        # method called by event handler when space bar pressed - adds a 'live' bullet to the list at curren gun position
        self.alive_bullets += [gun_pos]

    def on_hit(self, hit_bullet):
        # when a collision occurs, removes the relevant bullet from the alive_bullets list
        self.alive_bullets.remove(hit_bullet)

    def update(self):
        # iterates through the alive bullets list, updating positions based on velocity, and draws to screen
        for bullet in self.alive_bullets:
            bullet[0] += self.vx
            if bullet[0] > WIDTH:
                # removes bullets as they leave the screen
                self.alive_bullets.remove(bullet)
            Background.screen.blit(self.sprite, (bullet[0], bullet[1]))



class Alien:
    # loading the alien sprite and getting it's dimensions
    sprite = pyg.image.load(os.path.join("images", "alien.png"))
    ln = sprite.get_width()
    ht = sprite.get_height()

    def __init__(self):
        # initiates spawn position at the right of the screen
        self.x = WIDTH
        # alien velocity
        self.vx = -3
        # spawn rate - the SMALLER the number, the MORE OFTEN they spawn
        self.spawn_rate = 75
        # score for a kill
        self.kill_score = 20
        # score change if enemy gets through
        self.penalty = -10
        # a list of lists - each entry is the [x,y] co-ordinates of a 'live' alien
        self.alive_aliens = []

    def on_hit(self, hit_alien, Main):
        # when a collision occurs, removes the relevant alien from the alive_aliens list
        self.alive_aliens.remove(hit_alien)
        # updates score
        Main.update_score(self.kill_score)

    def update(self, Main):
        # generates a random integer between 1 and spawn_rate - if the number == 1, tries to spawn an alien
        if randint(1, self.spawn_rate) == 1:
            # uses a random integer to choose the y position to spawn - five possible tracks can be followed
            spawn_pos = [self.x, (randint(0,4) * (HEIGHT//5)) + BORDER]
            # runs a collision check to make sure the new alien won't spawn overlapping an existing alien
            spawn_collision = False
            spawn_hitbox = pyg.Rect(spawn_pos[0], spawn_pos[1], self.ln, self.ht)
            for alien in self.alive_aliens:
                alien_hitbox = pyg.Rect(alien[0], alien[1], self.ln, self.ht)
                if alien_hitbox.colliderect(spawn_hitbox):
                    spawn_collision = True
            if not spawn_collision:
                # adds the new 'live' alien to the alive_aliens list
                self.alive_aliens += [spawn_pos]
        # iterates through the alive_aliens list, updating positions based on velocity, and draws to screen
        for alien in self.alive_aliens:
            alien[0] += self.vx
            if alien[0] < (0-self.ln):
                # removes bullets as they leave the screen
                self.alive_aliens.remove(alien)
                # updates score
                Main.update_score(self.penalty)
            Background.screen.blit(self.sprite, (alien[0], alien[1]))

    def detect_collisions(self, Player, Bullet, Main):
        player_hitbox = Player.get_hitbox()
        # gets the list of alive bullets and the size of the bullets
        alive_bullets = Bullet.get_alive_bullets()
        bullet_size = Bullet.get_size()
        for alien in self.alive_aliens:
            # creates a hitbox for all the currently alive aliens
            alien_hitbox = pyg.Rect(alien[0], alien[1], self.ln, self.ht)
            for bull in alive_bullets:
                # creates a hitbox for all the currentlt alive bullets
                bullet_hitbox = pyg.Rect(bull[0], bull[1], bullet_size[0], bullet_size[1])
                # if the alien and bullet hitboxes collide, calls their relevant methods
                if alien_hitbox.colliderect(bullet_hitbox):
                    self.on_hit(alien, Main)
                    Bullet.on_hit(bull)
            # if the alien and player hitboxes collide, calls the player method, re-initialising the objects
            if alien_hitbox.colliderect(player_hitbox):
                Player.on_hit(self, Bullet, Main)