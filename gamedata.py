import pygame as pyg
import os
import time
from random import randint

# constants for the screen
WIDTH = 960
HEIGHT = 540
BORDER = 20

# Background object contains the display, and draws and updates the animated background
# Animation derived from instructions from the Nutt.net pygame tutoral
class Background(pyg.sprite.Sprite):
    screen = pyg.display.set_mode((WIDTH, HEIGHT), pyg.HWSURFACE)

    def __init__(self):
        pyg.sprite.Sprite.__init__(self)
        # loading the background image - two copies, to allow it to scroll
        self.bg1 = pyg.image.load(os.path.join("images", "background.jpg")).convert()
        self.bg2 = pyg.image.load(os.path.join("images", "background.jpg")).convert()
        self.bg1_x = 0
        self.bg2_x = self.bg1.get_width()

    def update(self):
        # updating the background positions so it scrolls
        self.bg1_x -= 1
        self.bg2_x -= 1
        if self.bg1_x <= -(self.bg1.get_width()):
                self.bg1_x = self.bg2_x + self.bg2.get_width()
        if self.bg2_x <= -(self.bg2.get_width()):
                self.bg2_x = self.bg1_x + self.bg1.get_width()

    def draw(self):
        self.screen.blit(self.bg1, (self.bg1_x, 0))
        self.screen.blit(self.bg2, (self.bg2_x, 0))


class Player(pyg.sprite.Sprite):
    # loading the player sprite and getting it's dimensions
    sprite = pyg.image.load(os.path.join("images", "hero_side.png")).convert_alpha()
    ln = sprite.get_width()
    ht = sprite.get_height()
    # loading the images for the sprite with animated thrusters
    animated_sprite = [pyg.image.load(os.path.join("images", "hero_side1.png")).convert_alpha(),
                       pyg.image.load(os.path.join("images", "hero_side2.png")).convert_alpha(),
                       pyg.image.load(os.path.join("images", "hero_side3.png")).convert_alpha()]

    def __init__(self):
        # sprite stuff, setting image, rectangle and mask (for collision detection)
        pyg.sprite.Sprite.__init__(self)
        self.image = self.sprite
        self.rect = self.image.get_rect()
        self.col_mask = pyg.mask.from_surface(self.image)
        # flag to hide the player image when player is killed
        self.hidden = False
        self.hide_timer = pyg.time.get_ticks()
        # initialises starting position on the board.
        self.x_new = self.rect.x = BORDER
        self.y_new = self.rect.y = HEIGHT//2 - self.ht
        self.speed = 4
        # animation loop - as it increments up, different images of the sprite are drawn, resulting in animation
        self.animation_loop = 0
        # x-axis velocity, used to determine whether to animate thrusters
        self.x_vel = 0
        self.altering_name = False
        self.player_name = ''

    def move(self, x_dir, y_dir):
        # takes the direction of movement from the event handler, multiplies by speed
        if (x_dir != 0) and (y_dir != 0):
            # this modifies the speed if moving diagonally
            velocity = int(self.speed * 0.8)
        else:
            velocity = self.speed
        # this step is here for animation purposes - it flags whether to animate thrusters
        self.x_vel = x_dir
        self.x_new = self.rect.x + (x_dir * velocity)
        self.y_new = self.rect.y + (y_dir * velocity)

    def update(self):
        # checks if the new positions are in the play area, and updates if they are
        if (self.x_new > BORDER) and (self.x_new < (WIDTH//2)):
            self.rect.x = self.x_new
        if (self.y_new > BORDER) and (self.y_new < HEIGHT-BORDER-self.ht):
            self.rect.y = self.y_new
        # if the player gets killed, hidden flag is true - hides player image, and resets position to starting point
        if self.hidden and pyg.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.x_new = self.rect.x = BORDER
            self.y_new = self.rect.y = HEIGHT//2 - self.ht
        # if player moving backwards, draws ship without thrusters
        if self.x_vel < 0:
            self.image = self.sprite
        # otherwise draws animated ship, and increments through animation loop
        else:
            self.image = self.animated_sprite[self.animation_loop//3]
            self.animation_loop += 1
            # reseting animation loop as only has three images to cycle through
            if self.animation_loop >= 9:
                self.animation_loop = 0

    def hide(self):
        # hide the player temporarily when the player is killed
        self.hidden = True
        self.hide_timer = pyg.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

    # logic for getting the user's name for the highscore board
    def update_name(self, new_letter="", delete=0):
        if not delete:
            self.player_name += new_letter
        else:
            self.player_name = self.player_name[:-1]


class Bullet(pyg.sprite.Sprite):
    # loading the bullet sprite and getting it's dimensions
    sprite = pyg.image.load(os.path.join("images", "bullet.png")).convert_alpha()
    ln = sprite.get_width()
    ht = sprite.get_height()

    def __init__(self):
        pyg.sprite.Sprite.__init__(self)
        self.image = self.sprite
        self.rect = self.image.get_rect()
        # bullet velocity
        self.vx = 15

    def update(self):
        self.rect.x += self.vx


class Alien(pyg.sprite.Sprite):
    # loading the alien sprite and getting it's dimensions
    sprite = pyg.image.load(os.path.join("images", "enemy2.png")).convert_alpha()
    ln = sprite.get_width()
    ht = sprite.get_height()
    animated_sprite = [pyg.image.load(os.path.join("images", "enemy1.png")).convert_alpha(),
                       pyg.image.load(os.path.join("images", "enemy2.png")).convert_alpha(),
                       pyg.image.load(os.path.join("images", "enemy3.png")).convert_alpha()]
    shielded_sprite = [pyg.image.load(os.path.join("images", "shield1.png")).convert_alpha(),
                       pyg.image.load(os.path.join("images", "shield2.png")).convert_alpha(),
                       pyg.image.load(os.path.join("images", "shield3.png")).convert_alpha()]

    def __init__(self, main):
        # pass main to alien, so it can access the player position and add alien bullets to the groups
        self.main = main
        # the sprite stuff, to get its image, rectangle and mask (for collision detection)
        pyg.sprite.Sprite.__init__(self)
        self.image = self.sprite
        self.rect = self.image.get_rect()
        self.col_mask = pyg.mask.from_surface(self.image)
        # sets the alien's position on the right of the screen, at a random y coordinate
        self.rect.x = WIDTH + self.ln + randint(1, 100)
        self.rect.y = randint(BORDER, HEIGHT - BORDER - self.ht)
        # alien velocity
        self.vx = -2
        # fire rate - the SMALLER the number, the MORE OFTEN they fire
        self.fire_rate = 400
        self.firing_solution = 1
        self.animation_loop = 0
        self.kill_score = 20
        # hit points - determines whether shield is up or down (displays different image)
        self.hitpoints = 1

    def collide(self, sprite_group):
        # collision detection only for when spawning new aliens, so they don't overlap
        if pyg.sprite.spritecollide(self, sprite_group, False):
            self.rect.x += self.ln * randint(2, 5)
            self.collide(sprite_group)

    def shoot(self, rate):
        # aliens fire based on fire_rate, adds alien bullets to the groups
        if (randint(1, rate) == self.firing_solution) and (self.rect.x < WIDTH):
            albull = AlBullet(self.rect.x, (self.rect.y + self.ht//2))
            self.main.alienbullets.add(albull)
            self.main.all_sprites.add(albull)

    def animate(self):
        if self.hitpoints == 2:
            self.image = self.shielded_sprite[self.animation_loop // 3]
        else:
            self.image = self.animated_sprite[self.animation_loop // 3]
        self.animation_loop += 1
        # reseting animation loop as only has three images to cycle through
        if self.animation_loop >= 9:
            self.animation_loop = 0

    def update(self):
        self.animate()
        # moves across the screen to the left, and fires
        self.rect.x += self.vx
        self.shoot(self.fire_rate)

    def on_hit(self, main, damage):
        self.hitpoints -= damage
        if self.hitpoints <= 0:
            self.kill()
            main.score += self.kill_score
            main.sounds.boom.play()
            main.expl = Explosion(self.rect.center, 'lg')
            main.all_sprites.add(main.expl)
        else:
            main.sounds.ping.play()


class ShieldAlien(Alien):
    def __init__(self, main):
        Alien.__init__(self, main)
        self.hitpoints = 2


class SmartAlien(ShieldAlien):

    def __init__(self, main):
        ShieldAlien.__init__(self, main)
        # limit the distance across the smart alien moves, and sets y velocity
        self.width_limit = WIDTH*0.8
        self.vy = 1
        # smart aliens fire more often than regular aliens
        self.fire_rate = 75

    def update(self):
        self.animate()
        # moves to the position on the right of the screen
        if self.rect.x > self.width_limit:
            self.rect.x += self.vx
        # tracks player movement and shoots
        if self.rect.y + self.ht//2 < self.main.player.rect.y + self.main.player.ht//2:
            self.rect.y += self.vy
        elif self.rect.y + self.ht//2 > self.main.player.rect.y + self.main.player.ht//2:
            self.rect.y -= self.vy
        self.shoot(self.fire_rate)


class Boss(SmartAlien):
    sprite = pyg.image.load(os.path.join("images", "boss1.png")).convert_alpha()
    damaged = [pyg.image.load(os.path.join("images", "boss5.png")).convert_alpha(),
               pyg.image.load(os.path.join("images", "boss4.png")).convert_alpha(),
               pyg.image.load(os.path.join("images", "boss3.png")).convert_alpha(),
               pyg.image.load(os.path.join("images", "boss2.png")).convert_alpha(),
               pyg.image.load(os.path.join("images", "boss1.png")).convert_alpha()]
    ln = sprite.get_width()
    ht = sprite.get_height()
    def __init__(self, main):
        SmartAlien.__init__(self, main)
        self.hitpoints = 50
        self.fire_rate = 40
        self.kill_score = 1000
        self.width_limit = WIDTH - self.ln

    def animate(self):
        if self.hitpoints < 50:
            self.image = self.damaged[self.hitpoints//10]
        bar = pyg.Rect((WIDTH//2 - 100), (HEIGHT - 20), 200, 18)
        healthbar = pyg.Rect((WIDTH//2 - 100), (HEIGHT - 19), self.hitpoints*4, 16)
        pyg.draw.rect(Background.screen, pyg.Color("black"), bar)
        pyg.draw.rect(Background.screen, pyg.Color("red"), healthbar)

    def update(self):
        if self.hitpoints > 15:
            SmartAlien.update(self)
        else:
            self.animate()
            new_x = self.rect.x + self.vx
            new_y = self.rect.y + self.vy
            if (new_x < 0) or (new_x > WIDTH-self.ln):
                self.vx = -self.vx
            if (new_y + self.ht//2 < BORDER) or (new_y + self.ht//2 > HEIGHT-BORDER):
                self.vy = -self.vy
            self.rect.x = new_x
            self.rect.y = new_y


class AlBullet(Bullet):
    # inherits most stuff from bullet, but moves right to left, and is slower
    def __init__(self, x, y):
        Bullet.__init__(self)
        self.rect.x = x
        self.rect.y = y
        self.vx = -10

# This class was built from instructions given in the pygame tutorial by KidsCanCode.org
class Explosion(pyg.sprite.Sprite):
    def __init__(self, center, size):
        pyg.sprite.Sprite.__init__(self)
        self.size = size
        self.frame = 0
        self.last_update = pyg.time.get_ticks()
        self.frame_rate = 50
        self.explosion_anim = {}
        self.explosion_anim['lg'] = []
        self.explosion_anim['sm'] = []
        for i in range(1,6):
            filename = 'boom{}.png'.format(i)
            img = pyg.image.load(os.path.join("images", filename)).convert_alpha()
            img_lg = pyg.transform.scale(img, (100, 100))
            self.explosion_anim['lg'].append(img_lg)
            img_sm = pyg.transform.scale(img, (75, 75))
            self.explosion_anim['sm'].append(img_sm)
        self.image = self.explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        now = pyg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


class PowerUp(pyg.sprite.Sprite):

    animated_life = [pyg.image.load(os.path.join("images", "hero_life.png")).convert_alpha(),
                     pyg.image.load(os.path.join("images", "hero_life1.png")).convert_alpha(),
                     pyg.image.load(os.path.join("images", "hero_life2.png")).convert_alpha()]

    animated_bombs = [pyg.image.load(os.path.join("images", "bomb1.png")).convert_alpha(),
                      pyg.image.load(os.path.join("images", "bomb2.png")).convert_alpha(),
                      pyg.image.load(os.path.join("images", "bomb3.png")).convert_alpha()]

    def __init__(self, main):
        self.main = main
        pyg.sprite.Sprite.__init__(self)
        self.spawned = False
        self.rewound = False
        self.powers_dict = {0: pyg.image.load(os.path.join("images", "1pixelimage.png")).convert_alpha(),
                            1: [self.animated_life, 93, 25, self.extra_life],
                            2: [self.animated_bombs, 58, 100, self.extra_bomb]}
        self.starttime = time.time()
        self.animation_loop = 0
        self.power_up = []
        self.spawn_pos = (0, 0)
        self.image = self.powers_dict[0]
        self.rect = self.image.get_rect()

    def update(self):
        if (time.time() - self.starttime)//1 == 3 and not self.spawned:
            # generate a random number between 1 and however many
            self.power_up = self.powers_dict[randint(1, 2)]
            self.image = self.power_up[0][0]
            self.rect = self.image.get_rect()
            self.rect.x = randint(BORDER, (WIDTH//2)-self.power_up[1])
            self.rect.y = randint(BORDER, HEIGHT-BORDER-self.power_up[2])
            self.spawned = True
        elif (time.time() - self.starttime)//1 == 10:
            self.starttime = time.time()
            self.image = self.powers_dict[0]
            self.rect.x = 0
            self.rect.y = 0
            self.spawned = False

        elif self.spawned:
            self.image = self.power_up[0][self.animation_loop // 3]
            self.animation_loop += 1
            if self.animation_loop >= 9:
                self.animation_loop -= 5
                self.rewound = True
            elif self.animation_loop >= 7 and self.rewound:
                self.animation_loop = 0
                self.rewound = False

    def extra_life(self):
        self.main.lives += 1

    def extra_bomb(self):
        self.main.bombs += 1
