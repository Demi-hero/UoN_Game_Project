import pygame as pyg
import os

image_dir = "PNGs"

class Character:
    def __init__(self):
        self.charsprite = pygame.image.load(os.path.join(image_dir, "Single_Old_Hero.PNG"))


player = Character()

print(type(player.charcter))
