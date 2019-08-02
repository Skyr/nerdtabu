import random
import yaml
import os
import os.path


class Settings:
    timeLimit = 45
    teams = ["Team A", "Team B"]
    score = [0, 0]
    questions = {}

    def __init__(self, quizfile, datadir):
        self.statefile_name = "{}.gamestate".format(quizfile.name)
        self.questions = yaml.safe_load(quizfile)
        self.datadir = datadir

    def get_random_cards(self):
        if os.path.isfile(self.statefile_name):
            with open(self.statefile_name, 'r') as infile:
                cards = list(yaml.safe_load_all(infile))
        else:
            cards = list(self.questions.keys())
            random.shuffle(cards)
        return cards

    def save_state(self, cards):
        if len(cards) > 0:
            with open(self.statefile_name, 'w') as outfile:
                yaml.safe_dump_all(cards, outfile)
        else:
            try:
                os.remove(self.statefile_name)
            except OSError:
                pass


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
