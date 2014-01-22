#!/usr/bin/env python2

import argparse
import time

import pygame

from settings import Settings
from theme import Theme


screen = None


def blit_centered(rect, elements, spacing):
    global screen
    total_height = (len(elements)-1) * spacing
    for el in elements:
        total_height = total_height + el.get_height()
    offset = rect.y + (rect.height - total_height)/2
    for i in range(len(elements)):
        el = elements[i]
        screen.blit(el, (rect.x + (rect.width - el.get_width())/2, offset))
        offset = offset + el.get_height() + spacing


def modify_settings(settings):
    pass


def display_scores(theme, settings):
    global screen

    team = theme.score_font.render(settings.teams[0], True, (255,255,255))
    score = theme.score_font.render(str(settings.score[0]), True, (255,255,255))
    blit_centered(theme.team_rect[0], [team, score], score.get_height()/4)

    team = theme.score_font.render(settings.teams[1], True, (255,255,255))
    score = theme.score_font.render(str(settings.score[1]), True, (255,255,255))
    blit_centered(theme.team_rect[1], [team, score], score.get_height()/4)


def team_get_ready(theme, settings, current_team):
    global screen
    screen.fill([0,0,0])
    screen.blit(theme.bg, (0,0))

    display_scores(theme, settings)

    info1 = theme.main_font.render(settings.teams[current_team], True, (255,0,0))
    info2 = theme.main_font.render("Get ready!", True, (255,0,0))
    blit_centered(theme.main_rect, [info1, info2], info1.get_height()/3)

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


def display_card(theme, settings, card):
    y = theme.main_rect.y

    info = theme.main_headline_font.render(card, True, (255,255,255))
    screen.blit(info, (theme.main_rect.x, y))
    y = y + info.get_height()*1.3

    for word in settings.questions[card]:
        info = theme.main_font.render(word, True, (255,255,255))
        screen.blit(info, (theme.main_rect.x, y))
        y = y + info.get_height() + 10


def repaint_round(theme, settings, card):
    screen.fill([0,0,0])
    screen.blit(theme.bg, (0,0))
    display_scores(theme, settings)
    display_card(theme, settings, card)
    pygame.display.update()


def play_round(theme, settings, current_team, cards):
    global screen
    opposite_team = (current_team+1)%len(settings.teams)
    start_time = time.time() * 1000
    round_time_left = settings.timeLimit * 1000
    last_sec_display = -1
    run_loop = True
    number_width = theme.number[0].get_width()
    is_paused = False

    card = cards.pop()
    repaint_round(theme, settings, card)

    while run_loop:
        time.sleep(0.01)
        if not is_paused:
            remaining_time = start_time + round_time_left - time.time() * 1000
            run_loop = (remaining_time > 0)
            if (int(remaining_time/1000)!=last_sec_display):
                # Update time display
                last_sec_display = int(remaining_time/1000)
                screen.blit(theme.number[(last_sec_display/10)%10],
                        (theme.countdown_rect.x, theme.countdown_rect.y))
                screen.blit(theme.number[last_sec_display%10],
                        (theme.countdown_rect.x + theme.countdown_rect.width - number_width, theme.countdown_rect.y))
                pygame.display.update(theme.countdown_rect)
                if (last_sec_display>10):
                    theme.clock_sound.play()
                elif (last_sec_display==0):
                    theme.clock_end_sound.play()
                else:
                    theme.clock_sound.play()
                    theme.clock_near_end_sound.play()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_loop = False
            elif event.type == pygame.KEYDOWN:
                if event.key==pygame.K_SPACE or event.key==pygame.K_p:
                    # Pause
                    is_paused = not is_paused
                    if is_paused:
                        round_time_left = remaining_time
                    else:
                        start_time = time.time() * 1000
                elif event.key==pygame.K_y or event.key==pygame.K_n:
                    if event.key==pygame.K_y:
                        # Correct
                        settings.score[current_team] = settings.score[current_team] + 1
                        theme.score_sound.play()
                    else:
                        # Oops
                        settings.score[opposite_team] = settings.score[opposite_team] + 1
                        theme.taboo_sound.play()
                    if len(cards)>0:
                        # Next card
                        card = cards.pop()
                        repaint_round(theme, settings, card)
                        last_sec_display = -1
                    else:
                        run_loop = False
                elif event.key==pygame.K_ESCAPE:
                    run_loop = False


def show_final_scores(theme, settings):
    global screen

    screen.fill([0,0,0])
    screen.blit(theme.bg, (0,0))

    display_scores(theme, settings)

    if (settings.score[0]==settings.score[1]):
        blit_centered(theme.main_rect, [ theme.main_font.render("It's a draw!", True, (255,0,0)) ], 0)
    else:
        winner_team = 0 if settings.score[0]>settings.score[1] else 1
        info1 = theme.main_font.render(settings.teams[winner_team], True, (255,0,0))
        info2 = theme.main_font.render("Congratulations!", True, (255,0,0))
        blit_centered(theme.main_rect, [ info1, info2 ], info1.get_height()/3)

    pygame.display.update()

    run_loop = True
    while run_loop:
        time.sleep(0.05)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_loop = False
            elif event.type == pygame.KEYDOWN:
                run_loop = False


def main():
    global screen
    print("Nerd Tabu")
    # Parse command line
    parser = argparse.ArgumentParser()
    parser.add_argument('quizfile', type=argparse.FileType('r'), help='Name of the quiz file')
    parser.add_argument('teamA', nargs='?', metavar='teamname_A', default='Team A', help='Name of team A')
    parser.add_argument('teamB', nargs='?', metavar='teamname_B', default='Team B', help='Name of team B')
    parser.add_argument('-d', '--datadir', default='.', help='Resource directory')
    parser.add_argument('-f', '--fullscreen', help='Run fullscreen', action='store_true')
    args = parser.parse_args()
    # Update settings
    settings = Settings(args.quizfile, args.datadir)
    settings.teams = [ args.teamA, args.teamB ]
    theme = Theme(args.datadir)
    # Initial game data
    cards = settings.get_random_cards()
    current_team = 0
    # Main game loop
    pygame.init()
    if args.fullscreen:
        screen = pygame.display.set_mode([1280,1024], pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode([1280,1024])
    theme.load_data()
    while len(cards)>0:
        team_get_ready(theme, settings, current_team)
        play_round(theme, settings, current_team, cards)
        current_team = (current_team + 1) % len(settings.teams)
    show_final_scores(theme, settings)
    pygame.quit()


if __name__ == "__main__":
    main()
