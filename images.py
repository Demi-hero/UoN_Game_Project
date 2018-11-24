import pygame as pyg
import os

background = os.path.join("images", "background.png")
pcship = os.path.join("images", "vipership.png")
npcship = os.path.join("images", "alien.png")


class Character:
    def __init__(self):
        self.charsprite = pyg.image.load(os.path.join(image_dir, "Single_Old_Hero.PNG"))


player = Character()

print(type(player.charsprite))
"""