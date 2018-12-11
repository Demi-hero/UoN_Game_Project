# The av class will go in here soon I hope
import pygame as pyg
import os
import csv

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
        self.pickup = pyg.mixer.Sound(os.path.join("sounds", "Power-Up.wav"))
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