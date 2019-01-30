import pygame
import sys
import random
from random import randint
from pygame.locals import *


class Paddle:
    def __init__(self, color, dims, y_change, surface):
        self.x = dims[0]
        self.y = dims[1]
        self.width = dims[2]
        self.height = dims[3]
        self.attributes = (self.x, self.y, self.width, self.height)
        self.color = color
        self.y_change = y_change
        self.surface = surface

    def update(self, direction):
        if direction == 'up' and self.y - self.y_change >= 0:
            self.y -= self.y_change
        elif direction == 'down' and self.y + self.y_change <= SCREEN_HEIGHT - self.height:
            self.y += self.y_change
        self.attributes = (self.x, self.y, self.width, self.height)
        return self.attributes

    def drawPaddle(self):
        pygame.draw.rect(self.surface, self.color, self.attributes)


class Ball:
    def __init__(self, surface, color, centre, radius, x_change, y_change):
        self.color = color
        self.x = centre[0]
        self.y = centre[1]
        self.centre = (self.x, self.y)
        self.radius = radius
        self.surface = surface
        self.right_end = self.x + self.radius
        self.left_end = self.x - self.radius
        self.lower_end = self.y + self.radius
        self.upper_end = self.y - self.radius
        self.x_change = x_change
        self.y_change = y_change

    def drawBall(self):
        pygame.draw.circle(self.surface, self.color, self.centre, self.radius)

    def update(self, paddle1_pos, paddle2_pos):

        if self.upper_end <= 0 or self.lower_end >= SCREEN_HEIGHT:
            self.y_change *= -1

        if self.upper_end >= paddle1_pos[1] and self.lower_end <= paddle1_pos[1] + paddle1_pos[3] and self.left_end <= paddle1_pos[0] + paddle1_pos[2] and self.right_end > paddle1_pos[0] + paddle1_pos[2]:
            self.x_change *= -1

        elif self.upper_end >= paddle2_pos[1] and self.lower_end <= paddle2_pos[1] + paddle2_pos[3] and self.right_end >= paddle2_pos[0] and self.left_end < paddle2_pos[0]:
            self.x_change *= -1

        elif self.right_end >= SCREEN_WIDTH or self.left_end <= 0:
            self.x = SCREEN_WIDTH // 2
            self.y = SCREEN_HEIGHT // 2
            self.y_change = random.choice((-1, 1, 3, -3, 2, -2))
            self.x_change = random.choice((-4, 4))

        self.x += self.x_change
        self.y += self.y_change
        self.centre = (self.x, self.y)
        self.right_end = self.x + self.radius
        self.left_end = self.x - self.radius
        self.lower_end = self.y + self.radius
        self.upper_end = self.y - self.radius


pygame.init()

# Setting Frame Rate of game
FPS = 120
fpsClock = pygame.time.Clock()

# Setting screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Defining colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Defining change in y coordinate of paddles due to single key press
paddle_ychange = 8

# Defining change in coordinates of ball over time
ball_xchange = 4
ball_ychange = 4

# Creating pygame surface
displaysurf = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pong!')
running = True

# Setting initial positions of both rectangular paddles
paddle1_pos = (20, 250, 15, 100)
paddle2_pos = (765, 250, 15, 100)

# Creating two paddle objects
paddle1 = Paddle(WHITE, paddle1_pos, paddle_ychange, displaysurf)
paddle2 = Paddle(WHITE, paddle2_pos, paddle_ychange, displaysurf)

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
        paddle1_pos = paddle1.update('up')
    if user_input[K_s]:
        paddle1_pos = paddle1.update('down')
    if user_input[K_UP]:
        paddle2_pos = paddle2.update('up')
    if user_input[K_DOWN]:
        paddle2_pos = paddle2.update('down')
    displaysurf.fill(BLACK)
    paddle1.drawPaddle()
    paddle2.drawPaddle()

    ball.update(paddle1_pos, paddle2_pos)
    ball.drawBall()

    pygame.display.update()
    fpsClock.tick(FPS)