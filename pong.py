import pygame, sys, time, random
from pygame.locals import *

# Set up pygame.
pygame.init()
mainClock = pygame.time.Clock()

# set up window
WINDOWWIDTH = 600
WINDOWHEIGHT = 400
BALL_SIZE = 16
window_surface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('PONG by Carlos Agustin')

# Setting up direction variables.
DOWN_LEFT = 'downleft'
DOWN_RIGHT = 'downright'
UP_LEFT = 'upleft'
UP_RIGHT = 'upright'

#MOVE_SPEED = 7

# Setting up the colors.
WHITE = (255, 255, 255)
RED =(255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# setting up ball
class Ball:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.change_x = 0
        self.change_y = 0

# makes a random ball
def make_ball():
    ball = Ball()

    # Set position
    ball.x = random.randrange(BALL_SIZE, WINDOWWIDTH - BALL_SIZE)
    ball.y = random.randrange(BALL_SIZE, WINDOWHEIGHT - BALL_SIZE)

    # Speed and direction
    ball.change_x = random.randrange(-4, 5)
    ball.change_y = random.randrange(-4, 5)

    return ball

# Adds ball to the game
ball_list = []
ball = make_ball()
ball_list.append(ball)



# setting up player.
player = pygame.Rect(200, 200, 40, 40)
player_image = pygame.image.load('apple_logo.png')

# Set up keyboard variables
move_left = move_right = move_up = move_down = False
MOVE_SPEED = 5

# Run the game loop.
while True:
    # Checks for QUIT event.
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        # Change the keyboard variables.
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                move_right = False
                move_left = True
            if event.key == K_RIGHT:
                move_right = True
                move_left = False
            if event.key == K_UP:
                move_down = False
                move_up = True
            if event.key == K_DOWN:
                move_down = True
                move_up = False
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_LEFT:
                move_left = False
            if event.key == K_RIGHT:
                move_right = False
            if event.key == K_UP:
                move_up = False
            if event.key == K_DOWN:
                move_down = False

   # Moving the player.
    if move_down and player.bottom < WINDOWHEIGHT:
        player.top += MOVE_SPEED
    if move_up and player.top > 0:
        player.top -= MOVE_SPEED
    if move_left and player.left > 0:
        player.left -= MOVE_SPEED
    if move_right and player.right < WINDOWWIDTH:
        player.right += MOVE_SPEED




    #  Draw the black background onto the surface.
    window_surface.fill(BLACK)

    for ball in ball_list:
        ball.x += ball.change_x
        ball.y += ball.change_y

        # makes ball bounce
        if ball.y > WINDOWHEIGHT - BALL_SIZE or ball.y < BALL_SIZE:
             ball.change_y *= -1
        if ball.x > WINDOWWIDTH - BALL_SIZE or ball.x < BALL_SIZE:
            ball.change_x *= -1
        if ball.x < player.width - BALL_SIZE:
            ball.change_x *= -1


    for ball in ball_list:
        pygame.draw.circle(window_surface, WHITE, [ball.x, ball.y], BALL_SIZE)
        window_surface.blit(player_image, player)

    # Displays the game
    pygame.display.update()
