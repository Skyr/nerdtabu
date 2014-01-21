import random

import yaml
import pygame

class Theme:
    number = [ ]
    bg = None
    team_rect = [ ]
    main_rect = None
    countdown_rect = None

    def __init__(self, datadir):
        self.datadir = datadir
        themedata = yaml.safe_load(open("%s/theme.yaml" % datadir, 'r'))
        self.team_rect = [ ]
        self.team_rect.append(pygame.Rect(themedata['team_a']['x'], themedata['team_a']['y'],
                themedata['team_a']['width'], themedata['team_a']['height']))
        self.team_rect.append(pygame.Rect(themedata['team_b']['x'], themedata['team_b']['y'],
                themedata['team_b']['width'], themedata['team_b']['height']))
        self.main_rect = pygame.Rect(themedata['main']['x'], themedata['main']['y'],
                themedata['main']['width'], themedata['main']['height'])
        self.countdown_rect = pygame.Rect(themedata['countdown']['x'], themedata['countdown']['y'],
                themedata['countdown']['width'], 0)

    def load_data(self):
        self.number = [ ]
        for n in range(10):
            self.number = self.number + [ pygame.image.load("%s/numbers/%d.png" % (self.datadir, n)).convert_alpha() ]
        self.bg = pygame.image.load("%s/screen.jpg" % self.datadir).convert()

