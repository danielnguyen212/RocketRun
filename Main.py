import pygame
import random
import math
import sys
import time
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((900, 700))

# Window title and icon
pygame.display.set_caption('Rocket Run')
window_icon = pygame.image.load('rocket.png')
pygame.display.set_icon(window_icon)

# Main menu background images and font
menu_background_image = pygame.image.load('menu_background.jpg')
menu_rocket_image = pygame.image.load('menu_rocket.png')
menu_title_font = pygame.font.SysFont('comicsans', 120, bold=True)

# Background image when playing the game
background_image = pygame.image.load('rocket_run_background.jpg')

# To override countdown number when it reaches 0
override_image = pygame.image.load('rocket_run_background_countdown_blit_override.jpg')

# Variables to give background a scrolling effect
backgroundY = 0
background_height = background_image.get_rect().height

# Game song
mixer.music.load('rocket_run_song.wav')
mixer.music.play(-1)

# Player
player_image = pygame.image.load('player_rocket.png')
playerX = 415
playerY = 470
playerX_change = 0

# Meteor
meteor_image = []
meteorX = []
meteorY = []
meteorY_change = []
num_of_meteors = 13

for i in range(num_of_meteors):
    meteor_image.append(pygame.image.load('meteor.png'))
    meteorX.append(random.randint(0, 836))
    meteorY.append(random.randint(-300, -50))

# Score
score_value = 0
score_textX = 10
score_textY = 10

# For countdown
start_time = 4
countdown_font = pygame.font.SysFont("timesnewroman", 64, bold=True)
countdown = True

# Colours
green = (0, 255, 0)
black = (0, 0, 0)
yellow = (255, 255, 0)

# Must declare for later functions
menu = True
retry = False


def player(x, y):
    screen.blit(player_image, (x, y))


def meteor(x, y, i):
    screen.blit(meteor_image[i], (x, y))


def collision_checker(meteorX, meteorY, playerX, playerY):
    collision_check = math.sqrt((math.pow(meteorX - playerX, 2)) + (math.pow(meteorY - playerY, 2)))
    if collision_check < 45:
        return True
    else:
        return False


def display_game_over():
    game_over_font = pygame.font.Font('freesansbold.ttf', 64)
    game_over_text = game_over_font.render("GAME OVER", True, green)
    screen.blit(game_over_text, (240, 230))


def display_score(x, y):
    score_font = pygame.font.Font('freesansbold.ttf', 32)
    score_text = score_font.render("SCORE: " + str(score_value), True, green)
    screen.blit(score_text, (x, y))


def easy_medium_hard_text():
    easy_font = pygame.font.SysFont('timesnewroman', 30, bold=True)
    easy_text = easy_font.render("EASY", True, yellow)
    screen.blit(easy_text, (185, 560))

    medium_font = pygame.font.SysFont('timesnewroman', 30, bold=True)
    medium_text = medium_font.render("MEDIUM", True, yellow)
    screen.blit(medium_text, (358, 560))

    hard_font = pygame.font.SysFont('timesnewroman', 30, bold=True)
    hard_text = hard_font.render("HARD", True, yellow)
    screen.blit(hard_text, (581, 560))


def arrow_keys():
    arrow_keys_image = pygame.image.load('arrow_keys.png')
    screen.blit(arrow_keys_image, (27, 150))
    left_arrow_key_image = pygame.image.load('left_arrow_key.png')
    screen.blit(left_arrow_key_image, (70, 310))
    right_arrow_key_image = pygame.image.load('right_arrow_key.png')
    screen.blit(right_arrow_key_image, (70, 420))


def instructions():
    first_instruction_font = pygame.font.SysFont("comicsans", 35, bold=False)
    first_instruction_text = first_instruction_font.render("Use arrow keys to dodge the meteors", True, yellow)
    screen.blit(first_instruction_text, (167, 205))

    second_instruction_font = pygame.font.SysFont("comicsans", 35, bold=False)
    second_instruction_text = second_instruction_font.render("Left arrow key moves rocket to the left", True, yellow)
    screen.blit(second_instruction_text, (120, 320))

    third_instruction_font = pygame.font.SysFont("comicsans", 35, bold=False)
    third_instruction_text = third_instruction_font.render("Right arrow key moves rocket to the right", True, yellow)
    screen.blit(third_instruction_text, (120, 430))


def main_menu():
    global menu, meteorY_change, num_of_meteors

    menu_title = menu_title_font.render("ROCKET RUN", True, (255, 60, 60))

    while menu:
        screen.blit(menu_background_image, (0, 0))
        screen.blit(menu_title, (125, 50))
        screen.blit(menu_rocket_image, (560, 160))
        arrow_keys()
        instructions()

        x, y = pygame.mouse.get_pos()

        easy_button = pygame.Rect(150, 550, 150, 50)
        pygame.draw.rect(screen, (255, 60, 60), easy_button, 7)

        medium_button = pygame.Rect(350, 550, 150, 50)
        pygame.draw.rect(screen, (255, 60, 60), medium_button, 7)

        hard_button = pygame.Rect(550, 550, 150, 50)
        pygame.draw.rect(screen, (255, 60, 60), hard_button, 7)

        easy_medium_hard_text()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_button.collidepoint(x, y):
                    if event.button == 1:
                        for i in range(num_of_meteors):
                            meteorY_change.append(3)
                        menu = False
                elif medium_button.collidepoint(x, y):
                    if event.button == 1:
                        for i in range(num_of_meteors):
                            meteorY_change.append(4.5)
                        menu = False
                elif hard_button.collidepoint(x, y):
                    if event.button == 1:
                        for i in range(num_of_meteors):
                            meteorY_change.append(6)
                        menu = False

        pygame.display.update()


def countdown_display():
    global countdown_font, countdown, start_time

    while countdown:

        screen.blit(background_image, (0, 0))

        player(playerX, playerY)

        for k in range(0, 4):
            start_time -= 1
            if start_time == 0:
                time.sleep(0.7)
                screen.blit(override_image, (352, 215))
                screen.blit(countdown_font.render("BLAST OFF!", True, green), (265, 315))
                pygame.display.update()
                time.sleep(0.7)
                countdown = False
            else:
                screen.blit(override_image, (352, 215))
                countdown_text = countdown_font.render(str(start_time), True, green)
                screen.blit(countdown_text, (430, 315))
                time.sleep(0.7)
                pygame.display.update()

        pygame.display.update()


def display_retry():
    global retry, num_of_meteors, score_value, meteor_image, meteorX, meteorY, meteorY_change, playerX, \
        playerY, playerX_change, menu, countdown, start_time, backgroundY, score_textX, score_textY

    screen.fill(black)
    screen.blit(background_image, (0, 0))
    rocket_explosion_image = pygame.image.load('rocket_explosion.png')
    screen.blit(rocket_explosion_image, (playerX - 85, playerY - 85))
    display_score(score_textX, score_textY)
    display_game_over()
    playerY = 5000

    retry_button = pygame.Rect(370, 320, 150, 50)
    retry_button_font = pygame.font.SysFont('timesnewroman', 30, bold=True)
    retry_button_text = retry_button_font.render("RETRY", True, (170, 250, 170))
    pygame.draw.rect(screen, (255, 60, 60), retry_button, 7)
    screen.blit(retry_button_text, (393, 328))

    while not retry:
        x, y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if retry_button.collidepoint(x, y):
                    if event.button == 1:
                        num_of_meteors = 13
                        score_value -= score_value
                        playerX = 415
                        playerY = 470
                        playerX_change = 0
                        start_time = 4
                        backgroundY = 0
                        meteorX.clear()
                        meteorY.clear()
                        meteorY_change.clear()

                        for i in range(num_of_meteors):
                            meteor_image.append(pygame.image.load('meteor.png'))
                            meteorX.append(random.randint(0, 836))
                            meteorY.append(random.randint(-300, -50))

                        menu = True
                        countdown = True
                        main()
                        retry = True

        pygame.display.update()


def main():
    global backgroundY, playerX, playerY, meteorX, meteorY, playerX_change, meteorY_change, num_of_meteors, score_value

    running = True

    while running:

        main_menu()

        if not menu:
            countdown_display()

        screen.fill(black)
        backgroundY_rel = backgroundY % background_height
        screen.blit(background_image, (0, backgroundY_rel - background_height))

        if backgroundY_rel < background_height:
            screen.blit(background_image, (0, backgroundY_rel))

        backgroundY += 2.5

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change += -6
                elif event.key == pygame.K_RIGHT:
                    playerX_change += 6
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

        playerX += playerX_change

        if playerX >= 836:
            playerX = 836
        elif playerX <= 0:
            playerX = 0

        for i in range(num_of_meteors):

            score_value += 1

            collision = collision_checker(meteorX[i], meteorY[i], playerX, playerY)

            if collision:
                explosion_sound = mixer.Sound('explosion.wav')
                explosion_sound.play()
                display_retry()

            if meteorY[i] >= 636:
                meteorX[i] = random.randint(0, 836)
                meteorY[i] = random.randint(-300, -50)

            meteorY[i] += meteorY_change[i]
            meteor(meteorX[i], meteorY[i], i)

        player(playerX, playerY)
        display_score(score_textX, score_textY)

        pygame.display.update()


main()
