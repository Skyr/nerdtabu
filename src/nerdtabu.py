#!/usr/bin/env python2

import argparse
import time

import pygame

from settings import Settings


screen = None


def modify_settings(settings):
    pass


def display_scores(settings):
    global screen
    font = pygame.font.SysFont("None", 32)

    team = font.render(settings.teams[0], True, (255,255,255))
    score = font.render(str(settings.score[0]), True, (255,255,255))
    screen.blit(team, (0,0))
    screen.blit(score, ((team.get_width() - score.get_width())/2, team.get_height() + 5))

    team = font.render(settings.teams[1], True, (255,255,255))
    score = font.render(str(settings.score[1]), True, (255,255,255))
    screen.blit(team, (screen.get_width()-team.get_width(), 0))
    screen.blit(score, (screen.get_width() - (team.get_width() + score.get_width())/2, team.get_height() + 5))


def team_get_ready(settings, current_team):
    global screen
    font = pygame.font.SysFont("None", 32)
    screen.fill([0,0,0])

    display_scores(settings)

    info1 = font.render(settings.teams[current_team], True, (255,0,0))
    info2 = font.render("Get ready!", True, (255,0,0))
    screen.blit(info1, ((screen.get_width() - info1.get_width())/2,100))
    screen.blit(info2, ((screen.get_width() - info2.get_width())/2,100 + info1.get_height() + 10))

    pygame.display.update()

    run_loop = True
    while run_loop:
        time.sleep(0.05)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_loop = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    modify_settings(settings)
                elif event.key == pygame.K_SPACE:
                    run_loop = False


def display_card(settings, card):
    answer_font = pygame.font.SysFont("None", 48)
    forbidden_font = pygame.font.SysFont("None", 32)
    y = settings.card_y

    info = answer_font.render(card, True, (255,255,255))
    screen.blit(info, (settings.card_x, y))
    y = y + info.get_height()*1.3

    for word in settings.questions[card]:
        info = forbidden_font.render(word, True, (255,255,255))
        screen.blit(info, (settings.card_x, y))
        y = y + info.get_height() + 10


def repaint_round(settings, card):
    screen.fill([0,0,0])
    display_scores(settings)
    display_card(settings, card)
    pygame.display.update()


def play_round(settings, current_team, cards):
    global screen
    opposite_team = (current_team+1)%len(settings.teams)
    start_time = time.time() * 1000
    round_time_left = settings.timeLimit * 1000
    last_sec_display = -1
    run_loop = True
    number_width = settings.number[0].get_width()
    number_height = settings.number[0].get_height()
    is_paused = False

    card = cards.pop()
    repaint_round(settings, card)

    while run_loop:
        time.sleep(0.01)
        if not is_paused:
            remaining_time = start_time + round_time_left - time.time() * 1000
            run_loop = (remaining_time > 0)
            if (int(remaining_time/1000)!=last_sec_display):
                # Update time display
                last_sec_display = int(remaining_time/1000)
                screen.blit(settings.number[(last_sec_display/10)%10],
                        (settings.countdown_x, settings.countdown_y))
                screen.blit(settings.number[last_sec_display%10],
                        (settings.countdown_x + number_width, settings.countdown_y))
                pygame.display.update((settings.countdown_x, settings.countdown_y,
                    2*number_width, number_height))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_loop = False
            elif event.type == pygame.KEYDOWN:
                if event.key==pygame.K_SPACE or event.key==pygame.K_p:
                    # Pause
                    is_paused = not is_paused
                    print is_paused
                    if is_paused:
                        round_time_left = remaining_time
                    else:
                        start_time = time.time() * 1000
                elif event.key==pygame.K_y or event.key==pygame.K_n:
                    if event.key==pygame.K_y:
                        # Correct
                        settings.score[current_team] = settings.score[current_team] + 1
                    else:
                        # Oops
                        settings.score[opposite_team] = settings.score[opposite_team] + 1
                    if len(cards)>0:
                        # Next card
                        card = cards.pop()
                        repaint_round(settings, card)
                    else:
                        run_loop = False
                elif event.key==pygame.K_ESCAPE:
                    run_loop = False


def show_final_scores(settings):
    pass


def main():
    global screen
    print("Nerd Tabu")
    # Parse command line
    parser = argparse.ArgumentParser()
    parser.add_argument('quizfile', type=argparse.FileType('r'), help='Name of the quiz file')
    parser.add_argument('teamA', nargs='?', metavar='teamname_A', default='Team A', help='Name of team A')
    parser.add_argument('teamB', nargs='?', metavar='teamname_B', default='Team B', help='Name of team B')
    parser.add_argument('--datadir', default='.', help='Resource directory')
    args = parser.parse_args()
    # Update settings
    settings = Settings(args.quizfile, args.datadir)
    settings.teams = [ args.teamA, args.teamB ]
    # Initial game data
    cards = settings.get_random_cards()
    current_team = 0
    # Main game loop
    pygame.init()
    screen = pygame.display.set_mode([1024,768]) # , pygame.FULLSCREEN)
    settings.load_data()
    while len(cards)>0:
        team_get_ready(settings, current_team)
        play_round(settings, current_team, cards)
        current_team = (current_team + 1) % len(settings.teams)
    show_final_scores(settings)
    pygame.quit()


if __name__ == "__main__":
    main()
