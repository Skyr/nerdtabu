#!/usr/bin/env python2

import argparse

import pygame

from settings import Settings


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

    pygame.quit()


if __name__ == "__main__":
    main()
