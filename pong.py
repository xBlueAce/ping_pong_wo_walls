import pygame, sys, time, random
from pygame.locals import *
from pygame.math import Vector2

# Set up pygame.
pygame.init()
mainClock = pygame.time.Clock()

# set up window
WINDOWWIDTH = 800
WINDOWHEIGHT = 400
BALL_SIZE = 16

window_surface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('PONG by Carlos Agustin')

# Setting up the colors.
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Setting up direction variables.
DOWN_LEFT = 'downleft'
DOWN_RIGHT = 'downright'
UP_LEFT = 'upleft'
UP_RIGHT = 'upright'

# Setting up the music
paddleNoise = pygame.mixer.Sound('sound6.wav')
win_sound = pygame.mixer.Sound('yay.wav')
lose_sound = pygame.mixer.Sound('focus.wav')
pygame.mixer.music.load('Take_Five.wav')
pygame.mixer.music.play(-1, 0.0)
musicPlaying = True

# Setting up score board.
player_score, AI_score = 0,0


# setting up text
basicFont = pygame.font.SysFont(None, 48)
player_text = basicFont.render('PLAYER: ' + str(AI_score), True, WHITE, None )
player_textRect = player_text.get_rect()
player_textRect.centerx = window_surface.get_rect().centerx = 600
player_textRect.centery = window_surface.get_rect().centery = 20

# Set up keyboard variables
move_left = move_right = move_up = move_down = False
MOVE_SPEED, BALL_SPEED, EZ_AI_SPEED = 5, 2, 3

# setting up player.
right_paddle = pygame.Rect((WINDOWWIDTH - 20), (WINDOWHEIGHT/2), 20, 100)
top_paddle = pygame.Rect((WINDOWWIDTH / 2) + (WINDOWWIDTH/4),0,100,20)
bottom_paddle = pygame.Rect((WINDOWWIDTH/2)+ (WINDOWWIDTH/4), WINDOWHEIGHT - 20,100,20)

# setting up AI.
left_AI_paddle = pygame.Rect(0,(WINDOWHEIGHT/2),20,100)
top_AI_paddle = pygame.Rect((WINDOWWIDTH / 2) - (WINDOWWIDTH/4),0,100,20)
bottom_AI_paddle = pygame.Rect((WINDOWWIDTH/2)- (WINDOWWIDTH/4), WINDOWHEIGHT - 20,100,20)

# setting up ball.
def vector2(xy_tuple, scale):    # work-around for macOs mojave unexpected args warning
    v = Vector2()
    v[0], v[1] = xy_tuple[0], xy_tuple[1]
    return v * scale

class Ball:
    def __init__(self, rect, bg_color, velocity, scale=1):
        self.bg_color_ = Color(bg_color)        # convert hex color string to Color
        self.rect_ = pygame.Rect(rect)    # convert rect tuple to pyGame.Rect
        self.velocity_ = vector2(velocity, scale)


    def __str__(self):
        return 'Box: clr={}, rect={}, velocity={}'.format(self.bg_color_, self.rect_, self.velocity_)

    def get_velocity(self):
        return self.velocity_

    def get_color(self):
        return self.bg_color_

    def get_rect(self):
        return self.rect_

    def move_box(self):
        self.rect_.left += self.velocity_[0]
        self.rect_.top += self.velocity_[1]
# makes a random ball
def make_ball():
    # Set position
    ball = Ball(rect=((random.randrange(BALL_SIZE, WINDOWWIDTH - BALL_SIZE)),(random.randrange(BALL_SIZE, WINDOWHEIGHT - BALL_SIZE)),20,20),
                bg_color='#FF0000',velocity=(1,1), scale=BALL_SPEED)


    return ball

# Adds ball to the game.
ball_list = []
ball = make_ball()
ball_list.append(ball)

intro_text = basicFont.render('score 7 to win', True, WHITE, None)

# Run the game loop.
while True:
    intro_text = basicFont.render('Must have two more points to win!', True, WHITE, None)
    intro_textRect = intro_text.get_rect()
    intro_textRect.centerx = window_surface.get_rect().centerx = 400
    intro_textRect.centery = window_surface.get_rect().centery = 200
    window_surface.blit(intro_text, intro_textRect)
    for event in pygame.event.get():
        # Check for the QUIT EVENT
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
                move_up = True
                move_down = False
            if event.key == K_DOWN:
                move_up = False
                move_down = True
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
            if event.key == K_m:
                if musicPlaying:
                    pygame.mixer.music.stop()
                else:
                    pygame.mixer.music.play(-1,0.0)
                    musicPlaying = not musicPlaying

    # Draws the black BackGround
    window_surface.fill(BLACK)

    # Draws in the center line
    pygame.draw.line(window_surface,WHITE,((WINDOWWIDTH/2),0),((WINDOWWIDTH/2),WINDOWHEIGHT), 4)

    # Move the player's paddles.
    if move_down and right_paddle.bottom < WINDOWHEIGHT:
        right_paddle.top += MOVE_SPEED
    if move_up and right_paddle.top > 0:
        right_paddle.top -= MOVE_SPEED
    if move_left and top_paddle.left > (WINDOWWIDTH/2):
        top_paddle.left -= MOVE_SPEED
        bottom_paddle.left -= MOVE_SPEED
    if move_right and top_paddle.right < WINDOWWIDTH:
        top_paddle.right += MOVE_SPEED
        bottom_paddle.right += MOVE_SPEED

    # setting ball in the game
    for ball in ball_list:
        r = ball.get_rect()
        v = ball.get_velocity()
        clr = ball.get_color()
        r.left += v[0]
        r.top += v[1]

        # bounces left or right
        if r.colliderect(left_AI_paddle) or r.colliderect(right_paddle):
            v[0] *= -1.001
            if musicPlaying:
                paddleNoise.play()
        # bounces up or down
        if r.colliderect(top_paddle) or r.colliderect(bottom_paddle) or r.colliderect(top_AI_paddle) or r.colliderect(bottom_AI_paddle):
            v[1] *= -1.001
            if musicPlaying:
                paddleNoise.play()

        # Draws circle
        pygame.draw.circle(window_surface, WHITE, [r.x, r.y], BALL_SIZE)


        # paddle going down
        if r.x < (WINDOWWIDTH / 2) and r.y > left_AI_paddle.y and left_AI_paddle.bottom < WINDOWHEIGHT:
            left_AI_paddle.top += EZ_AI_SPEED
        # paddle going up
        if r.x < (WINDOWWIDTH / 2) and r.y < left_AI_paddle.y and left_AI_paddle.top > 0:
            left_AI_paddle.top -= EZ_AI_SPEED
        # paddle going right
        if (WINDOWWIDTH / 2) > r.x > top_AI_paddle.x and top_AI_paddle.right < (WINDOWWIDTH / 2):
            top_AI_paddle.right += EZ_AI_SPEED
            bottom_AI_paddle.right += EZ_AI_SPEED
        # paddle going left
        if (WINDOWWIDTH / 2) > r.x and r.x < top_AI_paddle.x and top_AI_paddle.left > 0:
            top_AI_paddle.left -= EZ_AI_SPEED
            bottom_AI_paddle.left -= EZ_AI_SPEED

        # ball passes player (loss)
        if r.x > WINDOWWIDTH:
            r.x = 100
            r.y = 100
            AI_score += 1
            v = random.randrange(-1, 1), random.randrange(-1, 1)
            intro_text.fill(BLACK)
        if r.x < 0:
            r.x = 400
            r.y = 200
            # ball_list.clear()
            player_score += 1
            v = random.randrange(-1, 1), random.randrange(-1, 1)
            intro_text.fill(BLACK)
        if r.x > WINDOWWIDTH/2:
            if r.y < 0 or r.y > WINDOWHEIGHT:
                AI_score += 1
                r.x, r.y = 100,100
                v = random.randrange(-1, 1), random.randrange(-1, 1)
                intro_text.fill(BLACK)
        if r.x < WINDOWWIDTH/2:
            if r.y < 0 or r.y > WINDOWHEIGHT:
                player_score += 1
                r.x, r.y = 100, 100
                v = random.randrange(-1, 1), random.randrange(-1, 1)
                intro_text.fill(BLACK)

    # Draw text
    player_text = basicFont.render('PLAYER: ' + str(player_score), True, WHITE, None)
    player_textRect = player_text.get_rect()
    player_textRect.centerx = window_surface.get_rect().centerx = 600
    player_textRect.centery = window_surface.get_rect().centery = 40

    AI_text = basicFont.render('Computer: ' + str(AI_score), True, WHITE, None)
    AI_textRect = AI_text.get_rect()
    AI_textRect.centerx = window_surface.get_rect().centerx = 200
    AI_textRect.centery = window_surface.get_rect().centery = 40

    intro_text = basicFont.render('Must have at least 11 point \n and two more points to win!', True, WHITE, None)
    intro_textRect = intro_text.get_rect()
    intro_textRect.centerx = window_surface.get_rect().centerx = 400
    intro_textRect.centery = window_surface.get_rect().centery = 200

    # draw in text
    if( player_score or AI_score) == 0:
        window_surface.blit(intro_text, intro_textRect)
    window_surface.blit(player_text, player_textRect)
    window_surface.blit(AI_text, AI_textRect)

    # Draw the player's paddles.
    # right paddle
    pygame.draw.rect(window_surface, BLUE, right_paddle)
    # top paddle
    tb_paddle_image = pygame.image.load('design1.jpeg')# pygame.draw.rect(window_surface, GREEN, top_paddle)
    window_surface.blit(tb_paddle_image,top_paddle)
    window_surface.blit(tb_paddle_image,bottom_paddle)

    # Draw AI's Paddles.
    pygame.draw.rect(window_surface, WHITE, left_AI_paddle)
    pygame.draw.rect(window_surface, RED, top_AI_paddle)
    pygame.draw.rect(window_surface, RED, bottom_AI_paddle)

    # win
    if player_score >= AI_score + 2 and player_score > 10:
        win_text = basicFont.render('PLAYER WINS!', True, WHITE, None)
        win_textRect = win_text.get_rect()
        win_textRect.centerx, win_textRect.centery = 400,200
        window_surface.blit(win_text,win_textRect)
        ball_list.clear()
        if musicPlaying:
            win_sound.play()
    if AI_score >= player_score + 2 and AI_score > 10:
        win_text = basicFont.render('COMPUTER WINS!', True, WHITE, None)
        win_textRect = win_text.get_rect()
        win_textRect.centerx, win_textRect.centery = 400, 200
        window_surface.blit(win_text, win_textRect)
        ball_list.clear()
        if musicPlaying:
            lose_sound.play()

    # Draw the window onto the screen.
    pygame.display.update()
