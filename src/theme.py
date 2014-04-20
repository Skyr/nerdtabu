import random

import yaml
import pygame

class Theme:
    number = [ ]
    screen_size = [0,0]
    bg = None
    team_rect = [ ]
    main_rect = None
    countdown_rect = None
    score_font = None
    score_color = None
    main_headline_font = None
    main_headline_color = None
    main_font = None
    main_color = None
    horn_sound = None
    score_sound = None
    taboo_sound = None
    clock_sound = None
    clock_near_end_sound = None
    clock_end_sound = None

    def __init__(self, datadir):
        self.datadir = datadir
        self.themedata = yaml.safe_load(open("%s/theme.yaml" % datadir, 'r'))
        self.screen_size = [ self.themedata['screen']['width'], self.themedata['screen']['height'] ]
        self.team_rect = [ ]
        self.team_rect.append(pygame.Rect(self.themedata['team_a']['x'], self.themedata['team_a']['y'],
                self.themedata['team_a']['width'], self.themedata['team_a']['height']))
        self.team_rect.append(pygame.Rect(self.themedata['team_b']['x'], self.themedata['team_b']['y'],
                self.themedata['team_b']['width'], self.themedata['team_b']['height']))
        self.main_rect = pygame.Rect(self.themedata['main']['x'], self.themedata['main']['y'],
                self.themedata['main']['width'], self.themedata['main']['height'])
        self.countdown_rect = pygame.Rect(self.themedata['countdown']['x'], self.themedata['countdown']['y'],
                self.themedata['countdown']['width'], 0)

    def load_font(self, name):
        return pygame.font.Font("%s/%s" % (self.datadir, self.themedata[name]['name']), self.themedata[name]['size'])

    def get_color(self, name):
        return pygame.Color(self.themedata[name]['r'],self.themedata[name]['g'],  self.themedata[name]['b'])

    def load_sound(self, name):
        return pygame.mixer.Sound(file = "%s/%s" % (self.datadir, self.themedata[name]))

    def load_data(self):
        self.number = [ ]
        for n in range(10):
            self.number = self.number + [ pygame.image.load("%s/numbers/%d.png" % (self.datadir, n)).convert_alpha() ]
        self.countdown_rect = pygame.Rect(self.countdown_rect.x, self.countdown_rect.y,
                self.countdown_rect.width, self.number[0].get_width())
        self.bg = pygame.image.load("%s/screen.jpg" % self.datadir).convert()
        self.score_font = self.load_font("score_font")
        self.score_color = self.get_color("score_font")
        self.main_headline_font = self.load_font("main_headline_font")
        self.main_headline_color = self.get_color("main_headline_font")
        self.main_font = self.load_font("main_font")
        self.main_color = self.get_color("main_font")
        self.horn_sound = self.load_sound("horn_sound")
        self.score_sound = self.load_sound("score_sound")
        self.taboo_sound = self.load_sound("taboo_sound")
        self.clock_sound = self.load_sound("clock_sound")
        self.clock_near_end_sound = self.load_sound("clock_near_end_sound")
        self.clock_end_sound = self.load_sound("clock_end_sound")

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
