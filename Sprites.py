import pygame as pyg
import os
from random import randint

WIDTH = 960
HEIGHT = 540
BORDER = 10


class Background:
#    background = pyg.image.load(os.path.join("images", "background.jpg"))
    bg1 = pyg.image.load(os.path.join("images", "background.jpg"))
    bg2 = pyg.image.load(os.path.join("images", "background.jpg"))
    
    bg1_x = 0
    bg2_x = bg1.get_width()

class Player:
    # image is 205 by 43 px from side, 205 by 95 from top view
    ship = pyg.image.load(os.path.join("images", "hero_side.png"))
    shiptop = [pyg.image.load(os.path.join("images", "hero_top1.png")), 
               pyg.image.load(os.path.join("images", "hero_top2.png")), 
               pyg.image.load(os.path.join("images", "hero_top3.png"))]
    shipside = [pyg.image.load(os.path.join("images", "hero_side1.png")), 
               pyg.image.load(os.path.join("images", "hero_side2.png")), 
               pyg.image.load(os.path.join("images", "hero_side3.png"))]
    
    ht = 43
    ln = 205
    vx = 0
    vy = 0
    speed = 4
    vdiagmod = 0.8

    def __init__(self, x, y):
        self.x = x
        self.y = y-self.ht
        self.hitbox = pyg.Rect(self.x, self.y, self.ln, self.ht)
        self.lives = 3
        self.updown = False
        self.leftright = False
        self.flight_y = 0
        self.flight_x = 0

    # event handler?
    def on_hit(self):
        self.lives -= 1
        self.x = BORDER
        self.y = HEIGHT//2
        self.draw()
    # event handler


class Bullet:
    # image is 33 by 8 px
    bull = pyg.image.load(os.path.join("images", "bullet.png"))
    ht = 8
    ln = 33
    vx = 15
    gunposadj = [Player.ln*0.4, Player.ht*0.5]

    def __init__(self):
        self.x = 0
        self.y = 0
        self.alive = False
        self.hitbox = pyg.Rect(self.x, self.y, self.ln, self.ht)

    def fire(self, x, y):
        self.x = x + self.gunposadj[0]
        self.y = y + self.gunposadj[1]
        self.alive = True

    # needs to be in the event handler some how

class Alien:
    # image is 100 by 133 px
    ship = pyg.image.load(os.path.join("images", "alien.png"))
    ht = 100
    ln = 133
    vx = -3

    def __init__(self):
        self.x = WIDTH
        self.y = 0
        self.alive = False
        self.hitbox = pyg.Rect(self.x, self.y, self.ln, self.ht)

    def spawn(self):
        if self.alive == False:
            spawny = int(BORDER + (randint(0,4) * (HEIGHT*0.2)))
            self.y = spawny
        self.alive = True


background = Background()
player1 = Player(BORDER, HEIGHT//2)
aa = Bullet()
ab = Bullet()
ac = Bullet()
ad = Bullet()
ae = Bullet()
clip = [aa, ab, ac, ad, ae]
ba = Alien()
bb = Alien()
bc = Alien()
bd = Alien()
be = Alien()
bf = Alien()
bg = Alien()
bh = Alien()
bi = Alien()
swarm = [ba, bb, bc, bd, be, bf, bg, bh, bi]