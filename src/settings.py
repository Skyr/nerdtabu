import random

import yaml
import pygame

class Settings:
    timeLimit = 45
    teams = [ "Team A", "Team B" ]
    score = [ 0, 0 ]
    questions = { }
    number = [ ]
    card_x = 100
    card_y = 50
    countdown_x = 600
    countdown_y = 500

    def __init__(self, quizfile, datadir):
        self.questions = yaml.safe_load(quizfile)
        self.datadir = datadir

    def load_data(self):
        self.number = [ ]
        for n in range(10):
            self.number = self.number + [ pygame.image.load("%s/numbers/%d.png" % (self.datadir, n)).convert() ]

    def get_random_cards(self):
        cards = self.questions.keys()
        random.shuffle(cards)
        return cards

