import pygame
import sys
import random
from math import pi, sin, copysign
from random import randint
from pygame.locals import *


class Paddle:
    def __init__(self, color, dims, y_change, surface):
        self.x = dims[0]
        self.y = dims[1]
        self.width = dims[2]
        self.height = dims[3]
        self.attributes = (self.x, self.y, self.width, self.height)
        self.rect = pygame.Rect(self.attributes)
        self.color = color
        self.y_change = y_change
        self.surface = surface

    def update(self, direction, upperRect, lowerRect):
        if not self.rect.colliderect(upperRect) and direction == 'up':
            self.y -= self.y_change
        elif not self.rect.colliderect(lowerRect) and direction == 'down':
            self.y += self.y_change
        self.rect.y = self.y
        self.attributes = (self.x, self.y, self.width, self.height)

    def getRect(self):
        return self.rect

    def drawPaddle(self):
        pygame.draw.rect(self.surface, self.color, self.attributes)


class Ball:
    def __init__(self, surface, color, centre, radius, x_change, y_change):
        self.color = color
        self.x = centre[0]
        self.y = centre[1]
        self.centre = centre
        self.radius = radius
        self.surface = surface
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
        self.x_change = x_change
        self.y_change = y_change
        self.isHit = False
        self.isHitWall = False

    def drawBall(self):
        pygame.draw.circle(self.surface, self.color, self.centre, self.radius)

    def update(self, paddle1_rect, paddle2_rect, upperRect, lowerRect, leftRect, rightRect):

        if self.rect.colliderect(upperRect):
            self.y_change *= -1
            self.y = upperRect.bottom + self.radius
        elif self.rect.colliderect(lowerRect):
            self.y_change *= -1
            self.y = lowerRect.top - self.radius

        elif self.rect.colliderect(paddle1_rect) and not self.isHit:
            self.x_change *= -1
            top = paddle1_rect.top
            height = paddle1_rect.height
            angle = (5 * pi / 3) * ((self.y - top) / height) - 5 * pi / 6
            self.y_change = int(sin(angle) * 10)
            self.x = paddle1_rect.right + self.radius
            self.isHit = True

        elif self.rect.colliderect(paddle2_rect) and not self.isHit:
            global COLLISION_NUMBER
            self.x_change *= -1
            top = paddle2_rect.top
            height = paddle2_rect.height
            angle = (5 * pi / 3) * ((self.y - top) / height) - 5 * pi / 6
            self.y_change = int(sin(angle) * 10)
            self.x = paddle2_rect.left - self.radius
            self.isHit = True
            COLLISION_NUMBER += 1
            if COLLISION_NUMBER % 7 == 0:
                self.x_change = int(copysign(abs(self.x_change) + 2, self.x_change))

        elif self.rect.colliderect(leftRect) or self.rect.colliderect(rightRect):
            global SCORE1
            global SCORE2
            if self.rect.colliderect(rightRect):
                SCORE1 += 1
            else:
                SCORE2 += 1
            self.x = SCREEN_WIDTH // 2
            self.y = SCREEN_HEIGHT // 2
            self.y_change = random.choice((5, -5, -10, 10, 14, -14))
            self.x_change = random.choice((-10, 10))

        else:
            self.isHit = False

        self.x += self.x_change
        self.y += self.y_change
        self.centre = (self.x, self.y)
        self.rect.center = self.centre


def displayScore(displaysurf, value1, value2):
    fontObj = pygame.font.SysFont('ubuntu', 100)
    textSurfaceObj1 = fontObj.render(str(value1), True, WHITE, BLACK)
    textSurfaceObj2 = fontObj.render(str(value2), True, WHITE, BLACK)
    textRectObj1 = textSurfaceObj1.get_rect()
    textRectObj1.center = (300, 70)
    textRectObj2 = textSurfaceObj2.get_rect()
    textRectObj2.center = (500, 70)
    displaysurf.blit(textSurfaceObj1, textRectObj1)
    displaysurf.blit(textSurfaceObj2, textRectObj2)


def startScreen(displaysurf):
    displaysurf.fill(BLACK)
    fontObj1 = pygame.font.SysFont('ubuntu', 170)
    textSurfaceObj1 = fontObj1.render('PyPong', True, WHITE, BLACK)
    textRectObj1 = textSurfaceObj1.get_rect()
    textRectObj1.center = (400, 270)
    displaysurf.blit(textSurfaceObj1, textRectObj1)
    fontObj2 = pygame.font.SysFont('ubuntu', 40)
    textSurfaceObj2 = fontObj2.render('Press Space to Start', True, WHITE, BLACK)
    textRectObj2 = textSurfaceObj2.get_rect()
    textRectObj2.center = (400, 450)
    displaysurf.blit(textSurfaceObj2, textRectObj2)
    pygame.display.update()
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    intro = False
                    pygame.quit()
                    sys.exit()
                elif event.key == K_SPACE:
                    intro = False
            elif event.type == QUIT:
                pygame.quit()
                sys.exit()


def winScreen(displaysurf, winner):
    displaysurf.fill(BLACK)
    fontObj1 = pygame.font.SysFont('ubuntu', 100)
    textSurfaceObj1 = fontObj1.render('GAME OVER', True, WHITE, BLACK)
    textRectObj1 = textSurfaceObj1.get_rect()
    textRectObj1.center = (400, 270)
    displaysurf.blit(textSurfaceObj1, textRectObj1)
    fontObj2 = pygame.font.SysFont('ubuntu', 40)
    textSurfaceObj2 = fontObj2.render('PLAYER %d WINS!' % (winner), True, WHITE, BLACK)
    textRectObj2 = textSurfaceObj2.get_rect()
    textRectObj2.center = (400, 450)
    displaysurf.blit(textSurfaceObj2, textRectObj2)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == QUIT:
                pygame.quit()
                sys.exit()


def gameLoop():
    pygame.init()

    fpsClock = pygame.time.Clock()

    # Defining change in y coordinate of paddles due to single key press
    paddle_ychange = 20

    # Defining change in coordinates of ball over time
    ball_xchange = 10
    ball_ychange = 10

    # Creating pygame surface
    displaysurf = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Pong!')
    running = True

    startScreen(displaysurf)
    displaysurf.fill(BLACK)

    # Setting initial positions of both rectangular paddles
    paddle1_pos = (50, 250, 10, 100)
    paddle2_pos = (740, 250, 10, 100)

    leftRect = pygame.Rect(0, 0, 20, SCREEN_HEIGHT)
    rightRect = pygame.Rect(780, 0, 20, SCREEN_HEIGHT)
    upperRect = pygame.Rect(0, 0, SCREEN_WIDTH, 5)
    lowerRect = pygame.Rect(0, SCREEN_HEIGHT - 5, SCREEN_WIDTH, 5)

    # Creating two paddle objects
    paddle1 = Paddle(WHITE, paddle1_pos, paddle_ychange, displaysurf)
    paddle2 = Paddle(WHITE, paddle2_pos, paddle_ychange, displaysurf)

    paddle1_rect = paddle1.getRect()
    paddle2_rect = paddle2.getRect()
    # Drawing paddles to surface
    paddle1.drawPaddle()
    paddle2.drawPaddle()

    # Setting initial ball parameters
    ball_centre = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    ball_radius = 6

    # Creating ball object
    ball = Ball(displaysurf, WHITE, ball_centre, ball_radius, ball_xchange, ball_ychange)

    # Drawing ball
    ball.drawBall()

    # Game loop
    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == QUIT:
                pygame.quit()
                sys.exit()
        user_input = pygame.key.get_pressed()
        if user_input[K_w]:
            paddle1.update('up', upperRect, lowerRect)
        if user_input[K_s]:
            paddle1.update('down', upperRect, lowerRect)
        if user_input[K_UP]:
            paddle2.update('up', upperRect, lowerRect)
        if user_input[K_DOWN]:
            paddle2.update('down', upperRect, lowerRect)
        displaysurf.fill(BLACK)
        paddle1.drawPaddle()
        paddle2.drawPaddle()

        displayScore(displaysurf, SCORE1, SCORE2)
        if SCORE1 == 5:
            winScreen(displaysurf, 1)
        elif SCORE2 == 5:
            winScreen(displaysurf, 2)

        paddle1_rect = paddle1.getRect()
        paddle2_rect = paddle2.getRect()

        for i in range(-5, 601, 40):
            pygame.draw.rect(displaysurf, WHITE, (395, i, 10, 10))
        ball.update(paddle1_rect, paddle2_rect, upperRect, lowerRect, leftRect, rightRect)
        ball.drawBall()

        pygame.display.update()
        fpsClock.tick(FPS)


if __name__ == '__main__':

    # Setting screen dimensions
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

    # Defining colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    # Setting Frame Rate of game
    FPS = 40

    COLLISION_NUMBER = 0

    SCORE1 = 0
    SCORE2 = 0
    gameLoop()
