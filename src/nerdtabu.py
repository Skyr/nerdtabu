#!/usr/bin/env python2

import argparse
import time

import pygame

from settings import Settings


def team_get_ready(settings, current_team):
    font = pygame.font.SysFont("None", 32)
    settings.screen.fill([0,0,0])
    settings.screen.blit(font.render(settings.teams[current_team], True, (255,0,0)), (100,100))
    settings.screen.blit(font.render("Get ready!", True, (255,0,0)), (100,300))
    pygame.display.update()
    run_loop = True
    while run_loop:
        time.sleep(0.05)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_loop = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run_loop = False


def main():
    print("Nerd Tabu")
    # Parse command line
    parser = argparse.ArgumentParser()
    parser.add_argument('quizfile', type=argparse.FileType('r'), help='Name of the quiz file')
    parser.add_argument('teamA', nargs='?', metavar='teamname_A', default='Team A', help='Name of team A')
    parser.add_argument('teamB', nargs='?', metavar='teamname_B', default='Team B', help='Name of team B')
    args = parser.parse_args()
    # Update settings
    settings = Settings(args.quizfile)
    settings.teams = [ args.teamA, args.teamB ]
    # Initial game data
    cards = settings.get_random_cards()
    current_team = 0
    # Main game loop
    pygame.init()
    settings.screen = pygame.display.set_mode([1024,768])
    team_get_ready(settings, current_team)
    pygame.quit()


if __name__ == "__main__":
    main()
