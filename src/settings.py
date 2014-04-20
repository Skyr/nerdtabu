import random

import yaml
import pygame

class Settings:
    timeLimit = 45
    teams = [ "Team A", "Team B" ]
    score = [ 0, 0 ]
    questions = { }

    def __init__(self, quizfile, datadir):
        self.questions = yaml.safe_load(quizfile)
        self.datadir = datadir

    def get_random_cards(self):
        cards = self.questions.keys()
        random.shuffle(cards)
        return cards

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
