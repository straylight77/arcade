import pygame, sys, math, random
from pygame.locals import *

FPS = 30
MAX_X = 800
MAX_Y = 600

WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
GRAY      = (128, 128, 128)
DARKGRAY  = ( 40,  40,  40)
RED       = (255,  40,  40)
BGCOLOR = BLACK



class Paddle(pygame.sprite.Sprite):

    def __init__(self, arena):
        pygame.sprite.Sprite.__init__(self)
        self.load_sprite()
        self.rect = self.image.get_rect()
        self.rect.y = arena.bottom-50
        self.rect.x = arena.centerx - self.image.get_width()/2

    def load_sprite(self):
        self.image = pygame.Surface((70, 20))
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        pygame.draw.rect(self.image, GRAY, (10, 0, 50, 20))
        pygame.draw.circle(self.image, GRAY, (10, 10), 10)
        pygame.draw.circle(self.image, GRAY, (60, 10), 10)


    def update(self, arena, left, right):
        if left:
            self.rect.move_ip(-10, 0)
            if not arena.contains(self.rect):
                self.rect.left = arena.left
        if right:
            self.rect.move_ip(10, 0)
            if not arena.contains(self.rect):
                self.rect.right = arena.right


class Ball(pygame.sprite.Sprite):

    def __init__(self, arena):
        pygame.sprite.Sprite.__init__(self)
        self.load_sprite()
        self.rect = self.image.get_rect()
        self.rect.center = arena.center

    def load_sprite(self):
        self.image = pygame.Surface((16, 16))
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        pygame.draw.circle(self.image, GRAY, (8, 8), 8)


    def update(self, arena):
        self.rect.center = arena.center


def terminate():
    pygame.quit()
    sys.exit()

#### main ###############################################
pygame.init()
FPSCLOCK = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((MAX_X, MAX_Y))
BASICFONT = pygame.font.SysFont('courier', 15)
pygame.display.set_caption('pyGame Template')
random.seed()

#create sprites and groups

arena_rect = pygame.Rect(20, 20, MAX_X-220, MAX_Y-20)
paddle = pygame.sprite.GroupSingle( Paddle(arena_rect) )
balls = pygame.sprite.RenderPlain( Ball(arena_rect) )

cmd_left = False
cmd_right = False

while True:

    #event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()

        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                cmd_left = True
            elif event.key == K_RIGHT:
                cmd_right = True

        elif event.type == KEYUP:
            if event.key == K_ESCAPE:
                terminate()
            elif event.key == K_LEFT:
                cmd_left = False
            elif event.key == K_RIGHT:
                cmd_right = False



    #update game state
    paddle.update(arena_rect, cmd_left, cmd_right)
    balls.update(arena_rect)


    # draw frame
    DISPLAYSURF.fill(BGCOLOR)
    paddle.draw(DISPLAYSURF)
    balls.draw(DISPLAYSURF)

    pygame.draw.rect(DISPLAYSURF, RED, arena_rect, 1)
    #pygame.display.update()
    pygame.display.flip()
    FPSCLOCK.tick(FPS)

terminate()


