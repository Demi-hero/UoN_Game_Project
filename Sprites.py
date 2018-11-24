import pygame as pyg
import os

WIDTH = 960
HEIGHT = 540
BORDER = 10


class background:
    background = pyg.image.load(os.path.join("images", "background.png"))

class player:
    # image is 100 by 37 px
    ship = pyg.image.load(os.path.join("images", "vipership.png"))
    ht = 37
    ln = 100
    vx = 0
    vy = 0
    speed = 4
    vdiagmod = 0.8

    def __init__(self, x, y):
        self.x = x
        self.y = y-self.ht
        self.hitbox = pyg.Rect(self.x, self.y, self.ln, self.ht)
        self.lives = 3
    # event handler?
    def on_hit(self):
        self.lives -= 1
        self.x = BORDER
        self.y = HEIGHT//2
        self.draw()
    # event handler


class bullet:
    # image is 33 by 8 px
    bull = pyg.image.load(os.path.join("images", "bullet.png"))
    ht = 8
    ln = 33
    vx = 15
    gunposadj = [player.ln*0.4, player.ht*0.5]
    def __init__(self):
        self.x = 0
        self.y = 0
        self.alive = False
        self.hitbox = pyg.Rect(self.x, self.y, self.ln, self.ht)

    def fire(self, x, y):
        self.x = x + self.gunposadj[0]
        self.y = y + self.gunposadj[1]
        self.alive = True

class alien:
    # image is 88 by 36 px
    ship = pyg.image.load(os.path.join("images", "alien.png"))
    ht = 36
    ln = 88
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

    def update(self):
        if self.alive == True:
            self.x += self.vx
            self.hitbox = pyg.Rect(self.x, self.y, self.ln, self.ht)
            screen.blit(self.ship, (self.x, self.y))
        if self.x < (0-self.ln):
            self.alive = False
        if self.alive == False:
            self.x = WIDTH
            self.y = 0
            self.hitbox = pyg.Rect(self.x, self.y, self.ln, self.ht)


background = background()
player1 = player(BORDER, HEIGHT//2)
aa = bullet()
ab = bullet()
ac = bullet()
ad = bullet()
ae = bullet()
clip = [aa, ab, ac, ad, ae]
ba = alien()
bb = alien()
bc = alien()
bd = alien()
be = alien()
bf = alien()
bg = alien()
bh = alien()
bi = alien()
swarm = [ba, bb, bc, bd, be, bf, bg, bh, bi]