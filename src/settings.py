import yaml
import random

class Settings:
    timeLimit = 45
    teams = [ "Team A", "Team B" ]
    questions = { }

    def __init__(self, quizfile):
        self.questions = yaml.safe_load(quizfile)

    def get_random_cards(self):
        cards = self.questions.keys()
        random.shuffle(cards)
        return cards

