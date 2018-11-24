import pygame as pyg
import os
from random import randint

pyg.init()

# window details
WIDTH = 960
HEIGHT = 540
BORDER = 10
screen = pyg.display.set_mode((WIDTH, HEIGHT))
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
    def draw(self):
        self.hitbox = pyg.Rect(self.x, self.y, self.ln, self.ht)
        screen.blit(self.ship, (self.x, self.y))
    # event handler
    def update(self, pressedkeys):
        if pressedkeys[pyg.K_UP] and pressedkeys[pyg.K_LEFT]:
            self.vy = self.vx = -self.speed*self.vdiagmod
        elif pressedkeys[pyg.K_UP] and pressedkeys[pyg.K_RIGHT]:
            self.vy = -self.speed*self.vdiagmod
            self.vx = self.speed*self.vdiagmod
        elif pressedkeys[pyg.K_DOWN] and pressedkeys[pyg.K_RIGHT]:
            self.vy = self.vx = self.speed*self.vdiagmod
        elif pressedkeys[pyg.K_DOWN] and pressedkeys[pyg.K_LEFT]:
            self.vy = self.speed*self.vdiagmod
            self.vx = -self.speed*self.vdiagmod
        elif pressedkeys[pyg.K_UP]:
            self.vy = -self.speed
            self.vx = 0
        elif pressedkeys[pyg.K_DOWN]:
            self.vy = self.speed
            self.vx = 0
        elif pressedkeys[pyg.K_RIGHT]:
            self.vx = self.speed
            self.vy = 0
        elif pressedkeys[pyg.K_LEFT]:
            self.vx = -self.speed
            self.vy = 0
        else:
            self.vy = self.vx = 0
        newx = self.x + self.vx
        newy = self.y + self.vy
        if (newx > BORDER) and (newx < (WIDTH*0.66)):
            self.x=newx
        if (newy > BORDER) and (newy < HEIGHT-BORDER-self.ht):
            self.y = newy
        self.draw()


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

    def update(self):
        if self.alive:
            self.x += self.vx
            self.hitbox = pyg.Rect(self.x, self.y, self.ln, self.ht)
            screen.blit(self.bull, (self.x, self.y))
        if self.x > WIDTH:
            self.alive = False
        if not self.alive:
            self.x = 0
            self.y = 0
            self.hitbox = pyg.Rect(self.x, self.y, self.ln, self.ht)

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
running = True




def main():
    cooldown = 0
    spawn_rate = 1
    while running == True:
        screen.blit(background, (0, 0))
        ex = pyg.event.poll()
        if ex.type == pyg.QUIT:
            break
        pressedkeys = pyg.key.get_pressed()
        player1.update(pressedkeys)
        if pressedkeys[pyg.K_SPACE] and (cooldown == 0):
            for bullet in clip:
                if bullet.alive == False:
                    bullet.fire(player1.x, player1.y)
                    cooldown = 15
                    break
        for bullet in clip:
            bullet.update()
        if randint(1,75) <= spawn_rate:
            for alien in swarm:
                if alien.alive == False:
                    alien.spawn()
                    break
        for alien in swarm:
            alien.update()
            for bullet in clip:
                if alien.hitbox.colliderect(bullet.hitbox):
                    alien.alive = False
                    bullet.alive = False
            if alien.hitbox.colliderect(player1.hitbox):
                player1.on_hit()
                """if player1.lives == 0:
                    game_over()
                    break"""
        if cooldown > 0:
            cooldown -= 1
        pyg.display.flip()

    pyg.quit()
    os._exit(0)

"""
def game_over():
    for bullet in clip:
        bullet.alive = False
    for alien in swarm:
        alien.alive = False
    player1.lives = 3
    message = pyg.image.load(os.path.join("images", "game_over.png"))
    screen.blit(background, (0, 0))
    screen.blit(message, ((WIDTH-576)//2, (HEIGHT-195)//2))
    pyg.display.flip()
    while True:
        response = pyg.key.get_pressed()
        if response[pyg.K_y]:
            break"""

main()
