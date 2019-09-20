# Ryan Chen
# 893219394
# CPSC 386
#
# This program is Pong with no walls

import pygame
import sys
import time
from pygame.locals import *
from math import floor
import random

pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)

WINDOWWIDTH = 1280
WINDOWHEIGHT = 720
BALLWIDTH = 32
BALLHEIGHT = 32
BALLSTARTX = WINDOWWIDTH / 2
BALLSTARTY = WINDOWHEIGHT / 2
BALLSPEED = 20
BALLIMAGE = pygame.image.load('Images/ball.png')
PADDLESPEED = 5
PLAYERIMAGE = pygame.image.load('Images/player-texture.png')
COMPUTERIMAGE = pygame.image.load('Images/computer-texture.png')
BIGFONT = pygame.font.SysFont('Comic Sans MS', 128)

# Sounds
BOUNCE = pygame.mixer.Sound('Sounds/bounce.wav')
BIGWIN = pygame.mixer.Sound('Sounds/big-win.wav')
LITTLEWIN = pygame.mixer.Sound('Sounds/little-win.wav')
LOSE = pygame.mixer.Sound('Sounds/lose.wav')

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

surface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption("Pong")


class Ball:
    def __init__(self, rect, velocity, speed, image):
        self.rect_ = pygame.Rect(rect)
        self.velocity_ = pygame.math.Vector2(velocity[0] * speed, velocity[1] * speed)
        self.image_ = pygame.transform.scale(image, (self.rect_.width, self.rect_.height))

    def get_rect(self):
        return self.rect_

    def get_velocity(self):
        return self.velocity_

    def get_image(self):
        return self.image_

    def set_velocity(self, velocity):
        self.velocity_ = pygame.math.Vector2(velocity[0], velocity[1])

    def move(self):
        self.rect_.left += self.velocity_[0]
        self.rect_.top += self.velocity_[1]

    def bounce(self, component, friction):
        BOUNCE.play()
        self.velocity_[component % 1] += friction
        self.velocity_[component] *= -1


class Paddle:
    def __init__(self, rect, speed, image):
        self.rect_ = pygame.Rect(rect)
        self.speed_ = speed
        self.image_ = pygame.transform.scale(image, (self.rect_.width, self.rect_.height))

    def get_rect(self):
        return self.rect_

    def get_speed(self):
        return self.speed_

    def get_image(self):
        return self.image_

    def move(self, x, y):
        self.rect_.left += x * self.speed_
        self.rect_.top += y * self.speed_


def play_again(winner):
    win = BIGFONT.render(winner + " Wins", False, WHITE)
    win_rect = win.get_rect(center=(WINDOWWIDTH / 2, WINDOWHEIGHT / 4))

    prompt = BIGFONT.render("Play Again? Y / N", False, WHITE)
    prompt_rect = prompt.get_rect(center=(WINDOWWIDTH / 2, WINDOWHEIGHT / 2))

    surface.fill(BLACK)
    surface.blit(win, win_rect)
    surface.blit(prompt, prompt_rect)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running == False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                if event.key == pygame.K_y or event.key == pygame.K_KP_ENTER:
                    return True
                elif event.key == pygame.K_n or event.key == pygame.K_ESCAPE:
                    return False


def ball_init():
    rect_param = (BALLSTARTX, BALLSTARTY, BALLWIDTH, BALLHEIGHT)
    ball_velocity = pygame.math.Vector2(1 * random.choice((-1, 1)), 1 * random.choice((-1, 1)))
    ball_speed = random.randint(5, 7)
    ball = Ball(rect=rect_param, velocity=ball_velocity, speed=ball_speed, image=BALLIMAGE)
    return ball


def play():
    # Initialize Objects and parameters
    ball = ball_init()

    ptop = Paddle(rect=(WINDOWWIDTH * 0.75 - WINDOWWIDTH / 8, 32, WINDOWWIDTH / 8, 16),
                  speed=PADDLESPEED, image=PLAYERIMAGE)
    pbottom = Paddle(rect=(WINDOWWIDTH * 0.75 - WINDOWWIDTH / 8, WINDOWHEIGHT - 64, WINDOWWIDTH / 8, 16),
                     speed=PADDLESPEED, image=PLAYERIMAGE)
    pside = Paddle(rect=(WINDOWWIDTH - 64, WINDOWHEIGHT / 2 - WINDOWHEIGHT / 8, 16, WINDOWHEIGHT / 6),
                   speed=PADDLESPEED, image=PLAYERIMAGE)
    ctop = Paddle(rect=(WINDOWWIDTH * 0.25 - WINDOWWIDTH / 8, 32, WINDOWWIDTH / 8, 16),
                  speed=PADDLESPEED, image=COMPUTERIMAGE)
    cbottom = Paddle(rect=(WINDOWWIDTH * 0.25 - WINDOWWIDTH / 8, WINDOWHEIGHT - 64, WINDOWWIDTH / 8, 16),
                     speed=PADDLESPEED, image=COMPUTERIMAGE)
    cside = Paddle(rect=(32, WINDOWHEIGHT / 2 - WINDOWHEIGHT / 8, 16, WINDOWHEIGHT / 6),
                   speed=PADDLESPEED, image=COMPUTERIMAGE)
    empty_paddle = Paddle(rect=(0, 0, 0, 0), speed=0, image=COMPUTERIMAGE)

    last_bounce = empty_paddle
    paddles = [ptop, ctop, pbottom, cbottom, pside, cside]

    computer_score = 0
    player_score = 0
    computer_games = 2
    player_games = 2

    pygame.font.init()
    font = pygame.font.SysFont('Comic Sans MS', 128)
    computer_score_display = font.render(str(computer_score), False, WHITE)
    player_score_display = font.render(str(player_score), False, WHITE)

    move_left = move_right = move_up = move_down = False
    running = True

    clock = pygame.time.Clock()

    # Main loop
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running == False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    move_left = True
                    move_right = False
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    move_right = True
                    move_left = False
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    move_up = True
                    move_down = False
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    move_down = True
                    move_up = False
            elif event.type == pygame.KEYUP:
                if event.key == K_ESCAPE:
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    move_left = False
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    move_right = False
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    move_up = False
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    move_down = False

        # move objects
        ball.move()

        # player objects
        if move_up and pside.get_rect().top > 0:
            pside.move(0, -1)
        if move_down and pside.get_rect().bottom < WINDOWHEIGHT:
            pside.move(0, 1)
        if move_left and ptop.get_rect().left > WINDOWWIDTH / 2:
            ptop.move(-1, 0)
            pbottom.move(-1, 0)
        if move_right and ptop.get_rect().right < WINDOWWIDTH:
            ptop.move(1, 0)
            pbottom.move(1, 0)

        # computer objects
        if ball.get_rect().centery < cside.get_rect().centery and cside.get_rect().top >= 0:
            cside.move(0, -1)
        if ball.get_rect().centery > cside.get_rect().centery and cside.get_rect().bottom <= WINDOWHEIGHT:
            cside.move(0, 1)
        if ball.get_rect().centerx < ctop.get_rect().centerx and ctop.get_rect().left >= 0:
            ctop.move(-1, 0)
            cbottom.move(-1, 0)
        if ball.get_rect().centerx > ctop.get_rect().centerx and ctop.get_rect().right <= WINDOWWIDTH / 2:
            ctop.move(1, 0)
            cbottom.move(1, 0)

        # Collisions
        for p in paddles:
            if ball.get_rect().colliderect(p.get_rect()) and p != last_bounce:
                # Determine friction
                if p == pside or p == ptop or p == pbottom:
                    if move_up or move_left:
                        friction = -1
                    elif move_down or move_right:
                        friction = 1
                    else:
                        friction = 0
                else:
                    friction = 0

                # Do not bounce on same paddle
                last_bounce = p

                # Side bounces
                if p.get_rect().collidepoint(ball.get_rect().midleft):
                    ball.bounce(0, friction)
                    continue
                if p.get_rect().collidepoint(ball.get_rect().midright):
                    ball.bounce(0, friction)
                    continue
                if p.get_rect().collidepoint(ball.get_rect().midtop):
                    ball.bounce(1, friction)
                    continue
                if p.get_rect().collidepoint(ball.get_rect().midbottom):
                    ball.bounce(1, friction)
                    continue

                # Corner bounces
                if p.get_rect().collidepoint(ball.get_rect().bottomleft):
                    if p == pside or p == cside:
                        ball.bounce(0, friction)
                    else:
                        ball.bounce(1, friction)
                    continue
                if p.get_rect().collidepoint(ball.get_rect().bottomright):
                    if p == pside or p == cside:
                        ball.bounce(0, friction)
                    else:
                        ball.bounce(1, friction)
                    continue
                if p.get_rect().collidepoint(ball.get_rect().topleft):
                    if p == pside or p == cside:
                        ball.bounce(0, friction)
                    else:
                        ball.bounce(1, friction)
                    continue
                if p.get_rect().collidepoint(ball.get_rect().bottomleft):
                    if p == pside or p == cside:
                        ball.bounce(0, friction)
                    else:
                        ball.bounce(1, friction)
                    continue

        # wall collision
        if ball.get_rect().left <= 0:
            player_score += 1
            player_score_display = font.render(str(player_score), False, WHITE)
            last_bounce = empty_paddle
            ball = ball_init()
        if ball.get_rect().right >= WINDOWWIDTH:
            computer_score += 1
            computer_score_display = font.render(str(computer_score), False, WHITE)
            last_bounce = empty_paddle
            ball = ball_init()
        if ball.get_rect().top <= 0:
            if ball.get_rect().left < WINDOWWIDTH / 2:
                player_score += 1
                player_score_display = font.render(str(player_score), False, WHITE)
                last_bounce = empty_paddle
                ball = ball_init()
            else:
                computer_score += 1
                computer_score_display = font.render(str(computer_score), False, WHITE)
                last_bounce = empty_paddle
                ball = ball_init()
        if ball.get_rect().bottom >= WINDOWHEIGHT:
            if ball.get_rect().left < WINDOWWIDTH / 2:
                player_score += 1
                player_score_display = font.render(str(player_score), False, WHITE)
                last_bounce = empty_paddle
                ball = ball_init()
            else:
                computer_score += 1
                computer_score_display = font.render(str(computer_score), False, WHITE)
                last_bounce = empty_paddle
                ball = ball_init()

        if player_score >= 11 or computer_score >= 11:
            if player_score - computer_score >= 2:
                LITTLEWIN.play()
                player_games += 1
                player_score = 0
                computer_score = 0
                player_score_display = font.render(str(player_score), False, WHITE)
                computer_score_display = font.render(str(computer_score), False, WHITE)
            elif computer_score - player_score >= 2:
                LOSE.play()
                computer_games += 1
                player_score = 0
                computer_score = 0
                player_score_display = font.render(str(player_score), False, WHITE)
                computer_score_display = font.render(str(computer_score), False, WHITE)

        if player_games == 3:
            print("player won")
            BIGWIN.play()
            if play_again("Player"):
                computer_games = 0
                player_games = 0
            else:
                running = False
        elif computer_games == 3:
            print('computer won')
            if play_again("Computer"):
                computer_games = 0
                player_games = 0
            else:
                running = False

        # Draw objets
        surface.fill(BLACK)

        previous = 0
        for y in range(0, WINDOWHEIGHT):
            if y % 10 == 0:
                pygame.draw.line(surface, WHITE, (WINDOWWIDTH / 2, previous), (WINDOWWIDTH / 2, y), 4)
            previous = y

        surface.blit(computer_score_display, (WINDOWWIDTH * 0.25, WINDOWHEIGHT / 2 - 96))
        surface.blit(player_score_display, (WINDOWWIDTH * 0.75 - 96, WINDOWHEIGHT / 2 - 96))

        surface.blit(ball.get_image(), ball.get_rect())

        for p in paddles:
            surface.blit(p.get_image(), p.get_rect())

        pygame.display.update()


play()
