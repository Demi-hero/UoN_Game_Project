import pygame as pyg
import os
import time
from random import randint
from random import randrange
import csv
# push me harder
# constants for the screen
WIDTH = 960
HEIGHT = 540
BORDER = 10

#added 


class FileStore(pyg.sprite.Sprite):
    # class containing all the files that need loading in game that don't relate to an in game sprite.
    def __init__(self):
        self.load_data()
        pyg.sprite.Sprite.__init__(self)

    def load_data(self):
        self.scores = []
        self.background_music = os.path.join("sounds", "OrbitBeat130.wav")
        self.pewpew = pyg.mixer.Sound(os.path.join("sounds", "pew.wav"))
        self.boom = pyg.mixer.Sound(os.path.join("sounds", "boom.wav"))
        self.arrows = pyg.image.load(os.path.join("images", "PixelKeys2.png"))
        self.h = pyg.image.load(os.path.join("images", "h.png"))
        self.l = pyg.image.load(os.path.join("images", "L.png"))
        self.ult = pyg.mixer.Sound(os.path.join("sounds", "ult.wav"))
        self.space = pyg.image.load(os.path.join("images", "spacebar.png"))
        self.title = pyg.image.load(os.path.join("images", "Title.png"))
        # load in the high scores
        try:
            # have used with to double make sure I closed the file
            with open("highScore.csv", "r", newline='') as f:
                reader = csv.reader(f, delimiter=',')
                for row in reader:
                    self.scores.append(row)
                self.high_score = int(self.scores[0][1])
        except FileNotFoundError:
            self.create_false_hs()
        except ValueError:
            self.create_false_hs()
        except IndexError:
            self.create_false_hs()
        pyg.mixer.init()
        pyg.mixer.music.load(self.background_music)
        pyg.mixer.music.play(-1)

    def create_false_hs(self):
        with open("highscore.csv", "w", newline='') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=",")
            filewriter.writerow(["Jes", "300"])
            filewriter.writerow(["Peter", "200"])
            filewriter.writerow(["Nate", "100"])
            self.scores = [["Jes", "300"], ["Peter", "200"], ["Nate", "0"]]
            self.high_score = int(self.scores[0][1])

    def update_scores(self):
        for value, lists in enumerate(self.scores):
            if self.scoreboard[1] > int(lists[1]):
                self.scores.insert(value, self.scoreboard)
                break
        if len(self.scores) > 10:
            self.scores[:] = self.scores[:-1]
        with open("highscore.csv", "w", newline='') as f:
            scorewriter = csv.writer(f, delimiter=',')
            for lists in self.scores:
                scorewriter.writerow((lists[0], lists[1]))

# Background object contains the display, and draws and updates the animated background
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
    # this is the x-coordinate offset of the animated image, to account for it being longer due to the thrusters
#    animation_offset_x = ln - animated_sprite[0].get_width()

    def __init__(self):
        pyg.sprite.Sprite.__init__(self)
        self.ln = self.sprite.get_width()
        self.ht = self.sprite.get_height()
        self.image = self.sprite
        self.rect = self.image.get_rect()
        # change to a rect?
        self.radius = 100
        self.hidden = False
        self.hide_timer = pyg.time.get_ticks()

        # initialises starting position on the board.
        self.x_new = self.rect.x = BORDER
        self.y_new = self.rect.y = HEIGHT//2 - self.ht
        self.speed = 4
        # self.hitbox = pyg.Rect(self.x, self.y, self.ln, self.ht)

        # animation loop - as it increments up, different images of the sprite are drawn, resulting in animation
        self.animation_loop = 0

        # x-axis velocity, used to determine whether to animate thrusters
        self.x_vel = 0
        self.altering_name = False
        self.player_name = ''

#    def on_hit(self, Tokens, Main):
        # when player is hit, re-initialises the objects to clear the screen
#        for token in Tokens:
#            token.__init__()
        # updates number of lives
#        Main.update_lives(-1)


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
        # checks if the new positions are in the play area, and updates if they are

    def update(self):
        if (self.x_new > BORDER) and (self.x_new < (WIDTH//2)):
            self.rect.x = self.x_new
        if (self.y_new > BORDER) and (self.y_new < HEIGHT-BORDER-self.ht):
            self.rect.y = self.y_new
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
        # hide the player temporarily
        self.hidden = True
        self.hide_timer = pyg.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

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


def new_alien():
    alien = Alien()
    alien.collide(aliens)
    all_sprites.add(alien)
    aliens.add(alien)

class Alien(pyg.sprite.Sprite):
    sprite = pyg.image.load(os.path.join("images", "enemy2.png")).convert_alpha()
    ln = sprite.get_width()
    ht = sprite.get_height()
    # loading the alien sprite and getting it's dimensions
    animated_sprite = [pyg.image.load(os.path.join("images", "enemy1.png")).convert_alpha(),
              pyg.image.load(os.path.join("images", "enemy2.png")).convert_alpha(),
              pyg.image.load(os.path.join("images", "enemy3.png")).convert_alpha()]
    
    def __init__(self):
        pyg.sprite.Sprite.__init__(self)
        self.image = self.sprite
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH + self.ln + randint(1, 100)
        self.rect.y = randint(BORDER, HEIGHT - BORDER - self.ht)
        self.radius = 20
        # alien velocity
        self.vx = -4
        # spawn rate - the SMALLER the number, the MORE OFTEN they spawn
        self.spawn_rate = 100
        self.fire_rate = 200
        # score for a kill
        self.kill_score = 20
        # score change if enemy gets through
        self.penalty = -10
        self.animation_loop = 0

    def collide(self, sprite_group):
        if pyg.sprite.spritecollide(self, sprite_group, False):
            self.rect.x += self.ln * randint(2, 5)
            self.collide(sprite_group)

    def update(self):
        self.rect.x += self.vx       
        self.image = self.animated_sprite[self.animation_loop//3]
        self.animation_loop += 1
        # reseting animation loop as only has three images to cycle through
        if self.animation_loop >= 9:
            self.animation_loop = 0

'''
    def update(self, AlBullet, Main):
        # increases the spawn rate as player's score increases
        if (Main.score > 0) and (Main.score%300 == 0) and (self.spawn_rate > 15):
            self.spawn_rate -= 1
        # generates a random integer between 1 and spawn_rate - if the number == 1, tries to spawn an alien
        if randint(1, self.spawn_rate) == 1:
            # uses a random integer to choose the y position to spawn - five possible tracks can be followed
            spawn_pos = [self.rect.x, (randint(0,4) * (HEIGHT//5)) + BORDER]
            # runs a collision check to make sure the new alien won't spawn overlapping an existing alien
            spawn_collision = False
            for alien in self.alive_aliens:
                if (spawn_pos[1] == alien[1]) and (spawn_pos[0] <= alien[0]+self.ln):
                    spawn_collision = True
            if not spawn_collision:
                # adds the new 'live' alien to the alive_aliens list
                self.alive_aliens += [spawn_pos + [randint(1,2)]]
        # iterates through the alive_aliens list, updating positions based on velocity, and draws to screen
        for alien in self.alive_aliens:
            alien[0] += self.vx
            if alien[0] < (0-self.ln):
                # removes bullets as they leave the screen
                self.alive_aliens.remove(alien)
                # updates score
                Main.update_score(self.penalty)
            # aliens now shoot back at player
            if randint(1,self.fire_rate) == 1:
                AlBullet.fire([alien[0], alien[1]+self.ht//2])
    
   # def draw(self):
    #    for alien in self.alive_aliens:
     #       if alien[2] == 1:
      #          Background.screen.blit(self.sprite, (alien[0], alien[1]))
       #     else:
        #        Background.screen.blit(self.sprite2, (alien[0], alien[1]))

"""
    def detect_collisions(self, Tokens, Main):
        player_hitbox = Tokens[0].get_hitbox()
        # gets the list of alive bullets and the size of the bullets
        alive_bullets = Tokens[1].get_alive_bullets()
        bullet_size = Tokens[1].get_size()
        for alien in self.alive_aliens:
            # calculates if a collision has occurred between an alien and the player
            alien_hitbox = pyg.Rect(alien[0], alien[1], self.ln, self.ht)
            if alien_hitbox.colliderect(player_hitbox):
                Tokens[0].on_hit(Tokens, Main)
                return
            for bull in alive_bullets:
                # calculates if a collision has occurred between a bullet and alien
                if (bull[0]+bullet_size[0] >= alien[0]) and (bull[1] >= alien[1]-bullet_size[1]) and (bull[1] <= alien[1]+self.ht):
                    self.on_hit(alien, Main)
                    Tokens[1].on_hit(bull)
"""

class AlienSmart(Alien):

    def __init__(self):
        Alien.__init__(self)
        self.spawn_rate = 75
        self.fire_rate = 40
        self.speed = 1
        self.width_limit = WIDTH * 0.8

    def update(self, Player, AlBullet, Main):
        player_pos = Player.get_gun_location()
        if (randint(1, self.spawn_rate) == 1) and (self.alive_aliens == []):
            spawn_pos = [self.x, (randint(0,4) * HEIGHT//5) + BORDER]
            self.alive_aliens += [spawn_pos + [randint(1,2)]]
        for alien in self.alive_aliens:
            # moves to a point on the right of the screen
            if alien[0] > self.width_limit:
                alien[0] += self.vx
            # then tracks the player's y position
            if (alien[1]+self.ht//2) < player_pos[1]:
                self.vy = self.speed
            elif (alien[1]+self.ht//2) > player_pos[1]:
                self.vy = -self.speed
            else:
                self.vy = 0
            alien[1] += self.vy
            # shoots at the player
            if randint(1, self.fire_rate) == 1:
                AlBullet.fire([alien[0], alien[1]+self.ht//2])


class AlBullet(Bullet):

    def __init__(self):
        Bullet.__init__(self)
        self.vx = -10

    def fire(self, pos):
        self.alive_bullets += [pos]

#    def detect_collisions(self, Tokens, Main):
#        player_hitbox = Tokens[0].get_hitbox()
#        for bullet in self.alive_bullets:
#            bullet_hitbox = pyg.Rect(bullet[0], bullet[1], self.ln, self.ht)
#            if player_hitbox.colliderect(bullet_hitbox):
#                Tokens[0].on_hit(Tokens, Main)
'''
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

    def __init__(self, Main):
        pyg.sprite.Sprite.__init__(self)
        self.main = Main
        self.pickup = pyg.mixer.Sound(os.path.join("sounds", "Power-Up.wav"))
        self.spawned = False
        self.powers_dict = {0: [pyg.image.load(os.path.join("images", "hero_life.png")).convert_alpha(), 93, 25, self.extra_life],
                            1: [pyg.image.load(os.path.join("images", "bomb.png")).convert_alpha(), 58, 100, self.extra_bomb]}
        self.starttime = time.time()
        self.power_up = []
        self.spawn_pos = (0,0)

    def update(self):
        if (time.time() - self.starttime)//1 == 10 and not self.spawned:
            # generate a random number between 0 and however many
            self.power_up = self.powers_dict[randint(0, 1)]
            self.spawn_pos = (randint(BORDER, (WIDTH//2)-self.power_up[1]),
                              randint(BORDER, HEIGHT-BORDER-self.power_up[2]))
            self.hitbox = pyg.Rect(self.spawn_pos[0], self.spawn_pos[1], self.power_up[1], self.power_up[2])
            self.spawned = True
            Background.screen.blit(self.power_up[0],self.spawn_pos)
        elif (time.time() - self.starttime)//1 == 30:
            self.starttime = time.time()
            self.spawn_pos = (randint(BORDER, (WIDTH//2)-self.power_up[1]),
                              randint(BORDER, HEIGHT-BORDER-self.power_up[2]))
            self.spawned = False
#        elif self.spawned:
#            self.collection(player)
            if self.spawned:
                Background.screen.blit(self.power_up[0], self.spawn_pos)

    def extra_life(self):
        if self.spawned:
            self.main.lives += 1

    def extra_bomb(self):
        if self.spawned:
            self.main.bombs += 1
"""
    def collection(self, player):
        # how to tell when player and powerup hitboxes collied
        player_hitbox = player.get_hitbox()
        if self.hitbox.colliderect(player_hitbox):
            self.pickup.play()
            self.power_up[3]()
            self.spawned = False
"""            
all_sprites = pyg.sprite.Group()
aliens = pyg.sprite.Group()
# bullets = pyg.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    new_alien()